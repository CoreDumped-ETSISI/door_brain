from django.db import models


class Log(models.Model):
    message = models.CharField(max_length=1000, default='')
    date_time = models.DateTimeField(auto_now_add=True, primary_key=True)

    def __str__(self):
        if len(self.message) > 15:
            return self.message[0:15] + '... '
        else:
            return self.message
