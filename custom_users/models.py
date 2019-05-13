from django.db import models
from mqtt_groups.models import MqttGroup
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    mqtt_groups = models.ManyToManyField(MqttGroup)

    def __str__(self):
        return self.username
