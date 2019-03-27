from django.db import models
from custom_users.models import CustomUser


class Card(models.Model):
    hash = models.CharField(primary_key=True, max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.hash[0:3] + ' ' + self.user.username + ' (created at ' + self.created_at.strftime('%Y-%m-%d') + ')'
