from django.db import models
from mqtt_brokers.models import Broker


class Door(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    broker = models.ForeignKey(Broker, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.id
