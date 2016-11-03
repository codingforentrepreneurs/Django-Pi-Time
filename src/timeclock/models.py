from datetime import timedelta, datetime, time
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from django.utils import timezone



ACTIVITY_TIME_DETLA = getattr(settings, "ACTIVITY_TIME_DETLA", timedelta(minutes=1)) 



# https://docs.djangoproject.com/en/1.10/ref/exceptions/#django.core.exceptions.ValidationError
# Django Models Unleashed on http://joincfe.com

USER_ACTIVITY_CHOICES = (
        ('checkin', 'Check In'),
        ('checkout', 'Check Out'),
    )

class UserActivityQuerySet(models.query.QuerySet):
    def today(self):
        now = timezone.now()
        today_start = timezone.make_aware(datetime.combine(now, time.min))
        today_end  = timezone.make_aware(datetime.combine(now, time.max))
        return self.filter(timestamp__gte=today_start).filter(timestamp__lte=today_end)

    def checkin(self,):
        return self.filter(activity='checkin')

    def checkout(self,):
        return self.filter(activity='checkout')


    def current(self, user=None):
        if user is None:
            return self
        return self.filter(user=user).order_by('-timestamp').first()

class UserActivityManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return UserActivityQuerySet(self.model, using=self._db)

    def checkin(self):
        return self.get_queryset().checkin()

    def checkout(self):
        return self.get_queryset().checkout()

    def current(self, user=None):
        if user is None:
            return None
        current_obj = self.get_queryset().current(user)
        return current_obj

    def toggle(self, user=None):
        if user is None:
            return None
        last_item = self.current(user)
        activity = "checkin"
        if last_item is not None:
            now = timezone.now()
            diff = last_item.timestamp + ACTIVITY_TIME_DETLA
            if diff > now:
                return None
            if last_item.activity == "checkin":
                activity = "checkout"
        obj = self.model(
                user=user,
                activity = activity
            )
        obj.save()
        return obj

class UserActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    activity = models.CharField(max_length=120, default='checkin', choices=USER_ACTIVITY_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = UserActivityManager()
    abc = UserActivityManager()

    def __unicode__(self):
        return str(self.activity)

    def __str__(self):
        return str(self.activity)

    class Meta:
        verbose_name = 'User Activity'
        verbose_name_plural = "User Activities"

    @property
    def next_activity(self):
        next = "Check in"
        if self.activity == 'checkin':
            next = "Check out"
        return next

    @property
    def current(self):
        current = 'Checked Out'
        if self.activity == 'checkin':
            current = "Checked in"
        return current


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









