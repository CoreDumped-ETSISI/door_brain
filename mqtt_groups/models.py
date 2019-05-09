from django.db import models
from mqtt_rules.models import WeekRules


class MqttGroup(models.Model):
    name = models.CharField(primary_key=True, max_length=100, default=None)
    rules = models.ManyToManyField(WeekRules)
    initial_date = models.DateField(null=True)
    expiration_date = models.DateField(null=True)

    def __str__(self):
        return self.name
