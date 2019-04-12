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

PERMISSION_LEVEL = [
    (1, 'Ordinary'),
    (2, 'Events'),
    (3, 'Extraordinary')
]


class WeekRules(models.Model):
    initial_hour_access = models.TimeField(default=0)
    duration = models.DurationField(default=0)
    days_per_week = ArrayField(
        base_field=models.IntegerField(choices=WEEKDAYS)
    )
    expiration_date = models.DateField(null=True)
    initial_date = models.DateField(null=True)
    permission_level = models.IntegerField(choices=PERMISSION_LEVEL)
