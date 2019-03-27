from django.db import models
from custom_groups.models import CustomGroup


class CustomUser(models.Model):
    username = models.CharField(primary_key=True, max_length=100)
    group = models.ForeignKey(CustomGroup, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.username
