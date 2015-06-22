from django import forms
from django.core.exceptions import ValidationError
from .models import User


def validate_username(username):
        try:
            User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            return username
        raise ValidationError("%s is already taken." % username)


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=30, validators=[validate_username, ])
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField()  # widget=forms.PasswordInput(),
