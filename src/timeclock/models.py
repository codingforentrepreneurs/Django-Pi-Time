from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from django.utils import timezone


# https://docs.djangoproject.com/en/1.10/ref/exceptions/#django.core.exceptions.ValidationError
# Django Models Unleashed on http://joincfe.com

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

    class Meta:
        verbose_name = 'User Activity'
        verbose_name_plural = "User Activities"


    def clean(self, *args, **kwargs):
        if self.user:
            user_activites = UserActivity.objects.exclude(
                                id=self.id
                            ).filter(
                                user = self.user
                            ).order_by('-timestamp')
            if user_activites.exists():
                recent_ = user_activites.first()
                if self.activity == recent_.activity:
                    message = "%s is not a valid activity for this user" %(self.get_activity_display())
                    raise ValidationError(message)
                # check if timestamp is gte 10 minutes
            else:
                if self.activity != "checkin":
                    message = "%s is not a valid activity for this user as a first activity." %(self.get_activity_display())
                    raise ValidationError(message)

        return super(UserActivity, self).clean(*args, **kwargs)









