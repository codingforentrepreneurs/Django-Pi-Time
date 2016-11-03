from django.conf import settings
from django.db import models

from django.utils import timezone

# Create your models here.

# 1. Users
# 2. Daily Time Clock
# 3. In and Out per Day

# class UserDayTime(models.Model):
#     user =  models.ForeignKey(settings.AUTH_USER_MODEL)
#     today = models.DateField(default=timezone.now)


USER_ACTIVITY_CHOICES = (
        ('checkin', 'Check In'),
        ('checkout', 'Check Out'),
    )

class UserActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    activity = models.CharField(max_length=120, default='checkin', choices=USER_ACTIVITY_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.activity)

    def __str__(self):
        return str(self.activity)



