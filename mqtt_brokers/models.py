from django.db import models
from door_brain.settings import BROKER_DUTIES


class Broker(models.Model):
    ip = models.CharField(max_length=30, primary_key=True, default='X.X.X.X')
    duty = models.CharField(choices=BROKER_DUTIES.get("choices"), max_length=50)

    def __str__(self):
        return self.duty + ' - ' + self.ip
