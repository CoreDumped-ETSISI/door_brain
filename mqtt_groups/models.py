from django.db import models
from mqtt_rules.models import WeekRules
from django.core.exceptions import ValidationError
from datetime import time


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

    def get_time_table(self):
        time_table = {
            'L': [],
            'M': [],
            'X': [],
            'J': [],
            'V': [],
            'S': [],
            'D': []
        }
        rules = self.rules.get_queryset()
        for rule in rules:
            days = rule.days_per_week
            for day in days:
                init_time = rule.initial_hour_access
                final_hour = (init_time.hour + (rule.duration.seconds // 3600)) % 24
                final_minute = init_time.minute + ((rule.duration.seconds % 3600) // 60)
                final_time = time(hour=final_hour, minute=final_minute)
                time_period = [
                    init_time.strftime('%H:%M'),
                    final_time.strftime('%H:%M')
                ]
                time_table[day].append(time_period)
        return time_table
