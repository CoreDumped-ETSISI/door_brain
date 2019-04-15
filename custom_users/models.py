from django.db import models
from mqtt_groups.models import MqttGroup


class CustomUser(models.Model):
    username = models.CharField(primary_key=True, max_length=100, default=None)
    groups = models.ManyToManyField(MqttGroup)

    def __str__(self):
        return self.username
