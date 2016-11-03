from django.shortcuts import render

from django.views import View


from .models import UserActivity


# LOGIN REQUIRED
class ActivityView(View):
    def get(self, request, *args, **kwargs):
        # current activity
        obj = UserActivity.objects.current(request.user)
        return render(request, "timeclock/activity-view.html", {"object": obj})

    def post(self, request, *args, **kwargs):
        context = {}
        if request.user.is_authenticated():
            toggle = UserActivity.objects.toggle(request.user)
            context['object'] = toggle
        return render(request, "timeclock/activity-view.html", context)




# Django Class Based Views http://joincfe.com/projects
def activity_view(request, *args, **kwargs):
    # get
    if request.method == 'POST':
        # post 
        new_act = UserActivity.objects.create(user=request.user, activity='checkin')
    return render(request, "timeclock/activity-view.html", {})