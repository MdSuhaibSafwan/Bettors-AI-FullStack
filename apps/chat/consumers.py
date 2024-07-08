# import asyncio
from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from common.scripts import print_color
from django.conf import settings
from django.utils import timezone, dateformat
import json
from openai import OpenAI
from .adapters import GPTAssistant
import time

client = OpenAI(api_key=settings.OPENAI_API_KEY)
from typing import Generator
from .models import Room, Message
from .settings import MaxMessageTokens
from .utils import decompression, calc_token, is_tokens_less_than_settings
from asgiref.sync import sync_to_async, async_to_sync
from .utils import execute_sync_function


class OpenAIChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if settings.DEBUG:
            print_color("info: Run OpenAIChatConsumer.connect", 3)
        # group_add▽
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f'room_{self.room_id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        # group_add△
        print("Added to Group")
        await self.accept()

    async def disconnect(self, close_code):
        if settings.DEBUG:
            print_color("info: Run OpenAIChatConsumer.disconnect", 3)
        # group_discard▽
        # await self.channel_layer.group_discard(
        #                             self.room_group_name,
        #                             self.channel_name,)
        # group_discard△
        await self.close()
        # raise StopConsumer()

    async def receive(self, text_data=None, bytes_data=None):
        if settings.DEBUG:
            print_color("info: Run OpenAIChatConsumer.receive", 3)
        # Get post data
        text_data_json = json.loads(text_data)
        data_dict = decompression(text_data_json)
        # End of getting post data
        if settings.DEBUG:
            print_color(f"data_dict: {data_dict}", 3)
        # Catch the characters output by streaming
        llm_response = ""

        # Text to return when no question is asked
        if data_dict["user_sentence"].replace(" ", "").replace("　", "") == "":
            message_data = {
                "llm_answer": "You can ask questions like 'What bets are recommended for today?",
            }
            await self.send(json.dumps(message_data))
            if message_data["llm_answer"] is not None:
                llm_response += message_data["llm_answer"]

        # Text to return when no question is asked
        elif not is_tokens_less_than_settings(
            sentence=data_dict["user_sentence"]
            + data_dict["system_sentence"]
            + data_dict["assistant_sentence"],
            model_name=data_dict["model_name"],
            max_tokens=MaxMessageTokens,
        ):
            message_data = {
                "llm_answer": f"It seems that the number of characters entered has exceeded the set value.\nThe maximum token including system messages and assistant messages is set to {MaxMessageTokens}.",
            }
            await self.send(json.dumps(message_data))
            if message_data["llm_answer"] is not None:
                llm_response += message_data["llm_answer"]
        # Process when the token of the message exceeds the set value
        else:
            # Get history messages associated with the room
            history_message = await self.get_history(
                self.scope["url_route"]["kwargs"]["room_id"], data_dict["history_len"]
            )
            try:
                user = self.scope["user"]
                gpt = await execute_sync_function(GPTAssistant, user)
                self.gpt = gpt
                room = await self.get_room()
                is_room_expired = await execute_sync_function(func=room.check_expired)
                if is_room_expired:
                    message_data = {
                        "llm_answer": "This Room has been expired please create a new room",
                    }
                    await self.send(json.dumps(message_data))
                    return 
                user_msg = data_dict["user_sentence"]
                image_url = data_dict["image_url"]
                if image_url:
                    bot_response = await execute_sync_function(func=gpt.send_message_with_image, user=user, content=user_msg, 
                        image_url=image_url)

                    message_data = {
                        "llm_answer": bot_response,
                    }
                    await self.send(json.dumps(message_data))
                    return     
                message_obj = await execute_sync_function(func=gpt.add_message, thread_id=room.gpt_thread_id, content=user_msg)
                if isinstance(message_obj, str):
                    message_data = {
                        "llm_answer": message_obj,
                    }
                    await self.send(json.dumps(message_data))
                    return 

                run = await execute_sync_function(gpt.run_thread,  thread_id=room.gpt_thread_id)
                check = await execute_sync_function(gpt.check_run, run, room.gpt_thread_id)
                await execute_sync_function(gpt.get_response, thread_id=room.gpt_thread_id)
                llm_response = message_obj.llm_response           
            except ValueError as e:
                llm_response = str(e)

            message_data = {
                "llm_answer": llm_response,
            }
            await self.send(json.dumps(message_data))

            return 

            async for llm_answer in self.generater(
                data_dict["user_sentence"],
                data_dict["system_sentence"],
                data_dict["assistant_sentence"],
                history_message=history_message,
                model_name=data_dict["model_name"],
                max_tokens=data_dict["max_tokens"],
                temperature=data_dict["temperature"],
                top_p=data_dict["top_p"],
                presence_penalty=data_dict["presence_penalty"],
                frequency_penalty=data_dict["frequency_penalty"],
            ):
                message_data = {
                    "llm_answer": llm_answer,
                }
                print(message_data)  # print the response
                await self.send(json.dumps(message_data))
                if message_data["llm_answer"] is not None:
                    llm_response += message_data["llm_answer"]

        # Get additional information (consumed token number)
        response_info_dict = {
            "sent_tokens": calc_token(
                sentence=data_dict["user_sentence"]
                + data_dict["system_sentence"]
                + data_dict["assistant_sentence"],
                model_name=data_dict["model_name"],
            ),
            "generated_tokens": calc_token(
                sentence=llm_response, model_name=data_dict["model_name"]
            ),
        }
        # Save Model
        await self.save_message(data_dict, llm_response, response_info_dict)

    @database_sync_to_async
    def get_history(self, room_id, history_len):
        # Return None if the number of conversations to include in the history is 0
        if history_len == 0:
            return None
        else:
            return_history = ""
            message_objects = Message.objects.filter(room_id__room_id=room_id).order_by(
                "-date_create"
            )
            for i, message_object in enumerate(message_objects):
                # Control the number of conversations to include in the history
                if i + 1 >= history_len:
                    break
                return_history += "\n\n### Human: "
                return_history += message_object.user_message
                return_history += "\n### AI: "
                return_history += message_object.llm_response
                return_history += "\n### TimeStamp: "
                return_history += str(
                    dateformat.format(
                        timezone.localtime(message_object.date_create),
                        "Y-m-d H:i:s",  # Changed date format to English
                    )
                )
        return return_history

    @database_sync_to_async
    def get_room(self):
        room_id = self.scope["url_route"]["kwargs"]["room_id"]
        try:
            room = Room.objects.get(room_id=room_id)
        except Exception as e:
            return None

        return room

    @database_sync_to_async
    def save_message(self, data_dict, llm_response, response_info_dict):
        Message.objects.create(
            room_id=Room.objects.filter(room_id=self.room_id).first(),
            user_message=data_dict["user_sentence"],
            user_settings={
                k: v for k, v in data_dict.items() if k.lower() != "user_sentence"
            },
            llm_response=llm_response,
            response_info=response_info_dict,
        )

    # This is an asynchronous generator function that generates responses from the OpenAI API
    async def generater(
        self,
        user_sentence: str,
        system_sentence: str = None,
        assistant_sentence: str = None,
        *,
        history_message: str = None,
        model_name: str = "gpt-3.5-turbo",
        max_tokens: int = 256,
        temperature: float = 1.0,
        top_p: float = 1.0,
        presence_penalty: float = 1.0,
        frequency_penalty: float = 1.0,
    ) -> Generator[str, None, None]:
        # Check if the parameters are within the expected ranges
        if (
            not (0.0 <= temperature <= 2.0)
            or not (0.0 <= top_p <= 1.0)
            or not (-2.0 <= presence_penalty <= 2.0)
            or not (-2.0 <= frequency_penalty <= 2.0)
        ):
            # If any parameter is out of range, raise an error
            raise ValueError("llm parameter values error")

        # If there's a history message, prepend it to the user's sentence
        if history_message:
            _user_sentence = "Please answer in English. Answer the following questions as best you can.\n\nYou have refer to the following previous conversation historys:.\n\n## historys"
            _user_sentence += history_message
            _user_sentence += "\n\nLet's start a conversation.\n\n## Human: "
            _user_sentence += user_sentence
            _user_sentence += "\n\n## AI: "
            user_sentence = _user_sentence

        # Create the messages to send to the OpenAI API
        messages = [
            {
                "role": "system",
                "content": system_sentence
                if system_sentence != ""
                else f"You are a system admin.",
            },
            {
                "role": "user",
                "content": user_sentence,
            },
            {
                "role": "assistant",
                "content": assistant_sentence if assistant_sentence != "" else "",
            },
        ]

        # If debugging is enabled, print the messages
        if settings.DEBUG:
            print_color(f"messages: {messages}", 3)

        # Call the OpenAI API to generate responses
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
            stream=True,  # again, we set stream=True
        )

        collected_chunks = []
        collected_messages = []

        start_time = time.time()

        for chunk in response:
            chunk_time = (
                time.time() - start_time
            )  # calculate the time delay of the chunk
            collected_chunks.append(chunk)  # save the event response
            chunk_message = chunk.choices[0].delta.content  # extract the message
            yield chunk_message
            collected_messages.append(chunk_message)  # save the message

            # print the delay and text
            print(
                f"Message received {chunk_time:.2f} seconds after request: {chunk_message}"
            )  #

        # print the time delay and text received
        print(f"Full response received {chunk_time:.2f} seconds after request")

        collected_messages = [m for m in collected_messages if m is not None]
        full_reply_content = "".join([m for m in collected_messages])
        print(f"Full conversation received: {full_reply_content}")
