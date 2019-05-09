from django.db import models
from custom_users.models import User


class Card(models.Model):
    hash = models.CharField(primary_key=True, max_length=300, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    initial_date = models.DateField(null=True)
    expiration_date = models.DateField(null=True)

    def __str__(self):
        return self.hash[0:3] + ' ' + self.user.username + ' (created at ' + self.created_at.strftime('%Y-%m-%d') + ')'
