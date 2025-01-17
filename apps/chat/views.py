from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, ListView
from django.views.generic.edit import UpdateView, ModelFormMixin
from uuid import uuid4
from .models import Room, RoomSettings, Message
from .forms import RoomSettingsChangeForm, MessageImageForm
from .settings import (
    MaxHistoryLen,
    MinTokens,
    MaxTokens,
)
from .adapters import GPTAssistant
from .utils import save_file



class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = "apps/chat/room/list.html"
    context_object_name = "room_objects"

    def get_queryset(self):
        return self.model.objects.filter(create_user=self.request.user).order_by(
            "-date_create"
        )


class RoomView(LoginRequiredMixin, UpdateView):
    model = RoomSettings
    template_name = "apps/chat/room/room.html"
    fields = ("room_name",)

    def get_object(self):
        return get_object_or_404(
            self.model,
            room_id__create_user=self.request.user,
            room_id__room_id=self.kwargs["room_id"],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get a list of rooms associated with the user
        room_objects = Room.objects.filter(create_user=self.request.user).order_by(
            "-date_create"
        )

        # Get messages associated with the room
        message_objects = Message.objects.filter(
            room_id__room_id=self.kwargs["room_id"]
        ).order_by("date_create")

        context.update(
            {
                "room_settings_form": RoomSettingsChangeForm(**self.get_form_kwargs()),
                "room_objects": room_objects,
                "message_objects": message_objects,
                "MaxHistoryLen": MaxHistoryLen,
                "MinTokens": MinTokens,
                "MaxTokens": MaxTokens,
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        if "submit_room_settings_form" in request.POST:
            instance = get_object_or_404(
                self.model,
                room_id__create_user=self.request.user,
                room_id__room_id=self.kwargs["room_id"],
            )
            room_settings_form = RoomSettingsChangeForm(
                **self.get_form_kwargs(), instance=instance
            )
            if room_settings_form.is_valid():
                return self.form_valid(room_settings_form)
            else:
                self.object = self.get_object()
                return self.form_invalid(room_settings_form)
        else:
            return super().post(request, *args, **kwargs)

    def get_success_url(self):
        success_url = reverse_lazy(
            "chat:room", kwargs={"room_id": self.object.room_id.room_id}
        )
        return success_url


class RoomCreateView(LoginRequiredMixin, View):
    model = Room

    def get(self, request, *args, **kwargs):
        gpt = GPTAssistant(request.user)
        obj = gpt.create_room(request.user)
        reverse_url = reverse_lazy("chat:room", kwargs={"room_id": obj.room_id})
        return HttpResponseRedirect(reverse_url)


class RoomDeleteView(LoginRequiredMixin, View):
    model = Room

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(
            self.model,
            room_id=self.kwargs["room_id"],
            create_user=request.user,
        )
        obj.delete()
        return redirect("chat:room_list")


class ImageInsertView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        file = request.FILES.get("image", None)
        data = {}
        try:
            if file:
                path_url = save_file(file)
                data["url"] = path_url
                data["status_code"] = 200
                data["success"] = True
            else:
                data["status_code"] = 400
                data["message"] = "no image found"
        except ValueError as e:
            data = {
                "success": True,
                "message": e
            }
            return JsonResponse(data)
        return JsonResponse(data)
