from django.db import models

DUTIES = [
    ("logs", "doors logs listener"),
    ("management", "order publisher")
]


class Broker(models.Model):
    ip = models.CharField(max_length=30, primary_key=True)
    duty = models.CharField(choices=DUTIES, max_length=50)

    def __str__(self):
        return self.duty + ' - ' + self.ip
