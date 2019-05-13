from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models

WEEKDAYS = [
    ('L', 'Monday'),
    ('M', 'Tuesday'),
    ('X', 'Wednesday'),
    ('J', 'Thursday'),
    ('V', 'Friday'),
    ('S', 'Saturday'),
    ('D', 'Sunday')
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
        base_field=models.CharField(max_length=1, choices=WEEKDAYS),
    )

    def clean_fields(self, exclude=None):
        if isinstance(self.days_per_week, list):
            self.days_per_week = list(set(self.days_per_week))
