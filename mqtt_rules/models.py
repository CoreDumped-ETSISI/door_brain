from django.db import models
from django.contrib.postgres.fields import ArrayField

WEEKDAYS = [
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
    (7, 'Sunday')
]


class WeekRules(models.Model):
    identf = models.CharField(max_length=100, primary_key=True)
    initial_hour_access = models.TimeField(default=0)
    duration = models.DurationField(default=0)
    days_per_week = ArrayField(
        base_field=models.IntegerField(choices=WEEKDAYS)
    )
