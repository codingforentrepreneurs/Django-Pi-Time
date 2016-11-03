from django.shortcuts import render

from django.views import View


from .models import UserActivity


# LOGIN REQUIRED
class ActivityView(View):
    def get(self, request, *args, **kwargs):
        # current activity
        return render(request, "timeclock/activity-view.html", {})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            new_act = UserActivity.objects.create(user=request.user, activity='checkin')
        return render(request, "timeclock/activity-view.html", {})




# Django Class Based Views http://joincfe.com/projects
def activity_view(request, *args, **kwargs):
    # get
    if request.method == 'POST':
        # post 
        new_act = UserActivity.objects.create(user=request.user, activity='checkin')
    return render(request, "timeclock/activity-view.html", {})