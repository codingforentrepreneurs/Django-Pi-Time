from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


    def clean(self, *args, **kwargs):
        cleaned_data = super(LoginForm, self).clean(*args, **kwargs)
        username = cleaned_data['username']
        password = cleaned_data['password']
        qs = User.objects.filter(username__iexact=username)
        if not qs.exists() or qs.count() != 1:
            raise forms.ValidationError("This username/password is incorrect")
        else:
            user_obj = qs.first()
            if not user_obj.check_password(password):
                raise forms.ValidationError("This username/password is incorrect")
        return cleaned_data



    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data['username'] #.get('username')
        qs = User.objects.filter(username__iexact=username)
        if not qs.exists() or qs.count() != 1:
            raise forms.ValidationError("This username/password is incorrect")
        return username

    def clean_password(self, *args, **kwargs):
        username = self.cleaned_data['username'] #.get('username')
        password = self.cleaned_data['password']
        qs = User.objects.filter(username__iexact=username)
        if qs.exists() and qs.count() == 1:
            user_obj = qs.first()
            if not user_obj.check_password(password):
                raise forms.ValidationError("This username/password is incorrect")
            return password
        else:
            raise forms.ValidationError("This username/password is incorrect")


