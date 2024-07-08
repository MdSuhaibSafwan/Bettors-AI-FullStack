import json
import os
import time
import requests
import base64
import openai
from uuid import uuid4
from .models import Room, Message, MessageImage, Assistant, AssistantFunction
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from apps.payment.adapters import StripeAdapter
from apps.subscription.models import Subscription
from apps.payment.models import StripeCustomer
from openai import OpenAI
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


def get_image_as_base64(url):
    return base64.b64encode(requests.get(url).content)


def encode_image(image_path):
	  with open(image_path, "rb") as image_file:
	    return base64.b64encode(image_file.read()).decode('utf-8')


class GPTAssistant(object):

	def __init__(self, user):
		if not user.is_authenticated:
			raise ValueError("User UnAuthorized")
			
		api_key = os.environ.get("OPENAI_API_KEY")
		client = OpenAI(api_key=api_key)
		self.client = client
		self.user = user
		self.set_default_assistant()

	def set_default_assistant(self):
		assistant = Assistant.objects.get_default_assistant()
		self.assistant_obj = assistant
		self.assistant_id = assistant.model_id
		return assistant

	def get_assistant(self):
		return getattr(self, "assistant_obj", None)

	def create_room(self, user):
		try:
		    thread = self.client.beta.threads.create()

		except openai.BadRequestError as e:
			raise ValueError(e)

		except openai.APIConnectionError as e:
			raise ValueError(e)

		room = self.add_room_to_db(thread.id, user)
		return room

	def add_message(self, thread_id, content, file=None):
		if not self.is_user_valid_to_message(self.user):
			stripe_response = self.generate_message_for_user_with_payment_link(self.user)
			message_obj = self.add_user_message_to_db(self.user, content)
			self.add_gpt_message_to_db(message_obj, stripe_response)
			return stripe_response
			
		try:
			message = self.client.beta.threads.messages.create(
			    thread_id=thread_id,
			    role="user",
			    content=content
			)
		except openai.BadRequestError as e:
			raise ValueError(e)

		except openai.RateLimitError as e:
			raise ValueError(e)

		except openai.APIConnectionError as e:
			raise ValueError(e)

		except openai.InternalServerError as e:
			raise ValueError(e)

		message = self.add_user_message_to_db(self.user, content, thread_id=thread_id)
		return message

	def run_thread(self, thread_id, assistant_id=None):
		if self.assistant_id:
			assistant_id = self.assistant_id

		run = self.client.beta.threads.runs.create(
		  thread_id=thread_id,
		  assistant_id=assistant_id,
		  instructions=f"Please address the user as {self.user}. The user has a premium account."
		)
		return run

	def check_run_status(self, run, thread_id):
		try:
		    run = self.client.beta.threads.runs.retrieve(
		        thread_id=thread_id,
		        run_id=run.id
		    )

		except openai.APIConnectionError as e:
			raise ValueError(e)

		return run

	def check_run(self, run, thread_id):
		while True:
			run = self.check_run_status(run, thread_id)
			if run.status == "completed":
				print(f"Run is completed.")
				break
			
			elif run.status == "expired":
				print(f"Run is expired.")
				break

			elif run.status == "requires_action":
				print("Run requires Action.")
				self.manage_action_for_run(thread_id, run)
				
			else:
				print(f"OpenAI: Run is not yet completed. Waiting...{run.status} ")
				time.sleep(3)

		return run

	def manage_action_for_run(self, thread_id, run):
		tools_outputs_list = []

		tool_calls = run.required_action.submit_tool_outputs.tool_calls

		for tool_call in tool_calls:
			function_name = tool_call.function.name
			arguments = json.loads(tool_call.function.arguments)

			print("OpenAI: Calling Custom Function: ", function_name)

			try:
				assistant_function_obj = self.assistant_obj.assistantfunction_set.get(function_name=function_name)
			except ObjectDoesNotExist:
				print("Nothing Found")
				continue

			response = self.request_to_assistant_function(assistant_function_obj.endpoint)
			print(f"OpenAI: Getting response From Function {function_name}\n")

			tools_outputs_list.append({
				"tool_call_id": tool_call.id,
				"output": json.dumps(response)
			})


		self.inform_run_that_function_has_been_called(thread_id, run.id, tool_call.id, tools_outputs=tools_outputs_list)

	def inform_run_that_function_has_been_called(self, thread_id, run_id, tool_call_id, tools_outputs):
		try:
			run = self.client.beta.threads.runs.submit_tool_outputs(
			    thread_id=thread_id,
			    run_id=run_id,
			    tool_outputs=tools_outputs,
			)

		except openai.APIConnectionError as e:
			raise ValueError(e)

		return run

	def get_response(self, thread_id):
		try:
			messages = self.client.beta.threads.messages.list(
			  thread_id=thread_id
			)

		except openai.APIConnectionError as e:
			raise ValueError(e)

		gpt_response = messages.data[0].content[0].text.value
		self.gpt_response = gpt_response
		self.add_gpt_message_to_db(self.user_message_obj, gpt_response)
		return messages

	def get_or_create_room_for_user(self, user):
		self.user = user
		room = Room.objects.get_default_room(user)
		if room is None:
			room = self.create_room(user)

		return room

	def send_message_with_image(self, user, content, image_url):
		self.user = user
		base64_image = encode_image(image_url)
		api_key = os.environ.get("OPENAI_API_KEY")
		
		headers = {
		  "Content-Type": "application/json",
		  "Authorization": f"Bearer {api_key}"
		}

		payload = {
		  "model": "gpt-4-vision-preview",
		  "messages": [
		    {
		      "role": "user",
		      "content": [
		        {
		          "type": "text",
		          "text": content
		        },
		        {
		          "type": "image_url",
		          "image_url": {
		            "url": f"data:image/png;base64,{base64_image}"
		          }
		        }
		      ]
		    }
		  ],
		  "max_tokens": 300
		}

		r = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

		response = r.json()
		bot_response = response["choices"][0]["message"]["content"]

		message_obj = self.add_user_message_to_db(user, content)
		self.add_image(image_url, message_obj)
		self.add_gpt_message_to_db(message_obj, bot_response)
		return bot_response


	def add_room_to_db(self, gpt_thread_id, user):
		assistant_obj = self.get_assistant()
		room_id = uuid4().hex
		room = Room.objects.create(create_user=user, gpt_thread_id=gpt_thread_id, assistant_used=assistant_obj, room_id=room_id)
		return room

	def add_gpt_message_to_db(self, message_obj, gpt_response):
		message_obj.llm_response = gpt_response
		message_obj.save()
		return message_obj

	def add_user_message_to_db(self, user, user_msg, thread_id=None):
		if thread_id is None:
			room = Room.objects.get_default_room(user)
			if room is None:
				raise ValueError("No Room Found")
		else:
			try:
				room = Room.objects.get(
					Q(gpt_thread_id=thread_id),
				)
			except ObjectDoesNotExist as e:
				raise ValueError(e)

		obj = Message.objects.create(
			room_id=room, user_message=user_msg,
		)
		self.user_message_obj = obj
		return obj

	def add_image(self, image_url, message_obj):
		return MessageImage.objects.create(
			image_url=image_url,
			message=message_obj,
		)

	def request_to_assistant_function(self, endpoint):
		function_key = os.environ.get("OPENAI_FUNCTION_TOKEN")
		headers = {
			"Authorization": f"Bearer {function_key}"
		}
		r = requests.get(endpoint, headers=headers)
		if r.status_code == 500:
			raise ValueError("Function Call failed")

		if r.status_code in [400, 401, 402, 403, 404]:
			raise ValueError("Bad Request from Function Call")

		return r.json()

	def is_user_valid_to_message(self, user):
		if not user.is_authenticated:
			raise ValueError("User Un-Authorized")
		
		qs = user.usersubscription_set.order_by("-date_create")
		if qs.exists():
			obj = qs.first()
			has_expired = obj.has_expired()
			return not has_expired

		return False

	def generate_message_for_user_with_payment_link(self, user):
		stripe_adapter = StripeAdapter()
		text = stripe_adapter.create_text_for_payment_link_of_all_subscriptions(user)
		return text
