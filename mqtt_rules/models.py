from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models

WEEKDAYS = [
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
    (7, 'Sunday')
]


def validate_duration(duration):
    if duration.days != 0:
        raise ValidationError("Duration limit at 24 hours")


class WeekRules(models.Model):
    identf = models.CharField(max_length=100, primary_key=True)
    initial_hour_access = models.TimeField(default=0)
    duration = models.DurationField(default=0, validators=[validate_duration])
    days_per_week = ArrayField(
        size=7,
        base_field=models.IntegerField(choices=WEEKDAYS),
    )

    def clean_fields(self, exclude=None):
        self.days_per_week = list(set(self.days_per_week))
