from django.db import models
from door_brain.settings import BROKER_DUTIES


class Broker(models.Model):
    ip = models.CharField(max_length=30, default='X.X.X.X')
    port = models.IntegerField()
    duty = models.CharField(choices=BROKER_DUTIES.get("choices"), max_length=50)

    class Meta:
        unique_together = (("ip", "port", "duty"),)

    def __str__(self):
        return self.duty + ' - ' + self.ip
