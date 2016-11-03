from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View


from .forms import LoginForm, UserActivityForm
from .models import UserActivity


# LOGIN REQUIRED
class ActivityView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect("/login/")
        
        if request.session.get("username"):
            username_auth = request.user.username
            username_ses = request.session.get("username")
        if username_ses == username_auth:
            username = username_auth
            context = {}
            if username:
                form = UserActivityForm(initial={"username": username})
                context["form"] = form
                if request.user.is_authenticated():
                    obj = UserActivity.objects.current(request.user)
                    context['object'] = obj
        else:
            logout(request)
            return HttpResponseRedirect("/login/")
        return render(request, "timeclock/activity-view.html", context)

    def post(self, request, *args, **kwargs):
        form = UserActivityForm(request.POST)
        obj = UserActivity.objects.current(request.user)
        context = {"form": form, "object": obj}
        if form.is_valid():
            toggle = UserActivity.objects.toggle(request.user)
            context['object'] = toggle            
            return HttpResponseRedirect("/")
        return render(request, "timeclock/activity-view.html", context)


class UserLoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        context = {
            "form": form
        }
        return render(request, "timeclock/login-view.html", context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['username'] = username
            return HttpResponseRedirect("/")
        context = {"form": form}
        return render(request, "timeclock/login-view.html", context)



class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect("/")


# Django Class Based Views http://joincfe.com/projects
def activity_view(request, *args, **kwargs):
    # get
    if request.method == 'POST':
        # post 
        new_act = UserActivity.objects.create(user=request.user, activity='checkin')
    return render(request, "timeclock/activity-view.html", {})