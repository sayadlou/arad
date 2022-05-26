from captcha.fields import CaptchaField
from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm

from .widget import CustomCaptchaTextInput


# class AuthAdminForm(AuthenticationForm):
#     captcha = CaptchaField(widget=CustomCaptchaTextInput(attrs={'class': "form-control"}))



