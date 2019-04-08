from django.db import models
from mqtt_brokers.models import Broker
from custom_groups.models import CustomGroup


class Door(models.Model):
    id = models.CharField(max_length=100, primary_key=True, default=None)
    logs_broker = models.ForeignKey(Broker, on_delete=models.SET_NULL, null=True, related_name='logs')
    manage_broker = models.ForeignKey(Broker, on_delete=models.SET_NULL, null=True, related_name='management')
    groups = models.ManyToManyField(CustomGroup)

    def __str__(self):
        return self.id
