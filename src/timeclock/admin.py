from django.contrib import admin

# Register your models here.
from .models import UserActivity
# from timeclock.models import UserActivity

class UserActivityAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'user__email']
    list_display = ['user', 'activity', 'timestamp']
    list_filter = ['timestamp']
    class Meta:
        model = UserActivity


admin.site.register(UserActivity, UserActivityAdmin)