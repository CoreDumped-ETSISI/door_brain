from django.db import models


class CustomGroup(models.Model):
    name = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return self.name
