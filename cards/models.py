from django.db import models
from custom_users.models import User
from django.core.exceptions import ValidationError


class Card(models.Model):
    hash = models.CharField(primary_key=True, max_length=300, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    initial_date = models.DateField(null=True)
    expiration_date = models.DateField(null=True)

    def clean_fields(self, exclude=None):
        if self.initial_date >= self.expiration_date:
            raise ValidationError("Expiration date must be greater than initial date")

    def __str__(self):
        return self.hash[0:3] + ' ' + self.user.username + ' (created at ' + self.created_at.strftime('%Y-%m-%d') + ')'
