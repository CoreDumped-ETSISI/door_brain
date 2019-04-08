from django.db import models
from doors.models import Door


class Log(models.Model):
    card_authorized = models.BooleanField(default=False)
    reason = models.CharField(max_length=1000, default='')
    date_time = models.DateTimeField(default=None)
    door = models.ForeignKey(Door, on_delete=models.SET_NULL, null=True)
    card_hash = models.CharField(max_length=300, default=None)

    class Meta:
        unique_together = (("date_time", "door"),)

    def __str__(self):
        msg = self.date_time.strftime('%m-%d %H:%M')
        msg += ' '
        msg += 'AUTHORIZED ' if self.card_authorized else 'DENIED '
        msg += 'in door ' + self.door.id
        return msg
