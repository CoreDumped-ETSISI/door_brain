from django.db import models
from mqtt_brokers.models import Broker
from mqtt_groups.models import MqttGroup
from door_brain.settings import BROKER_DUTIES
from django.core.exceptions import ValidationError


def validate_manage_broker(broker_id):
    broker = Broker.objects.get(id=broker_id)
    if broker.duty != BROKER_DUTIES.get('MANAGEMENT'):
        raise ValidationError("manage_broker must have management as duty")


def validate_logs_broker(broker_id):
    broker = Broker.objects.get(id=broker_id)
    if broker.duty != BROKER_DUTIES.get('LOGS'):
        raise ValidationError("manage_broker must have logs_listener as duty")


class Door(models.Model):
    id = models.CharField(max_length=100, primary_key=True, default=None)
    logs_broker = models.ForeignKey(
        Broker,
        on_delete=models.SET_NULL,
        null=True,
        related_name='logs',
        validators=[validate_logs_broker]
    )
    manage_broker = models.ForeignKey(
        Broker,
        on_delete=models.SET_NULL,
        null=True,
        related_name='management',
        validators=[validate_manage_broker]
    )
    manage_topic = models.CharField(max_length=100)
    groups = models.ManyToManyField(MqttGroup)

    def __str__(self):
        return self.id
