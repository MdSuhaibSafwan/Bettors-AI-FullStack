from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


class DefaultManager(models.Manager):

	def get_queryset(self):
		qs = super().get_queryset().filter(deleted_at=None)
		return qs

	def get_deleted_objects(self):
		qs = super().get_queryset().filter(~Q(deleted_at=None))
		return qs		


class AssistantManager(DefaultManager):

    def get_default_assistant(self):
        try:
            obj = self.get(default=True)
        except MultipleObjectsReturned as e:
            raise ValueError(e)
        except ObjectDoesNotExist as e:
            raise ValueError(e)

        return obj


class RoomManager(DefaultManager):

	def get_default_room(self, user, **kwargs):
		qs = self.get_queryset().filter(expired_at=None, create_user=user, **kwargs)
		if not qs.exists():
			return None

		obj = qs.last()
		qs = qs.filter(~Q(id=obj.id))
		if qs.exists():
			qs.update(expired_at=timezone.now())

		return obj

