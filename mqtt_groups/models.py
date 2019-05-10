from django.db import models
from mqtt_rules.models import WeekRules
from django.core.exceptions import ValidationError


class MqttGroup(models.Model):
    name = models.CharField(primary_key=True, max_length=100, default=None)
    rules = models.ManyToManyField(WeekRules)
    initial_date = models.DateField(null=True)
    expiration_date = models.DateField(null=True)

    def clean_fields(self, exclude=None):
        if self.initial_date >= self.expiration_date:
            raise ValidationError("Expiration date must be greater than initial date")

    def __str__(self):
        return self.name
