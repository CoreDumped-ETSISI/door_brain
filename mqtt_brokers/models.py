from django.db import models


class Broker(models.Model):
    ip = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return self.ip
