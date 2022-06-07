from django import forms
from django.contrib.auth import password_validation, login
from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordResetForm, PasswordChangeForm, \
    SetPasswordForm
from django.utils.translation import gettext_lazy as _
from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile
from .widget import CustomCaptchaTextInput


class MyAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': "form-control"}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': "form-control"}),
    )
    captcha = CaptchaField(widget=CustomCaptchaTextInput(attrs={'class': "form-control"}))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': "form-control"})
    )
    captcha = CaptchaField(widget=CustomCaptchaTextInput(attrs={'class': "form-control"}))


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': "form-control", 'autocomplete': 'current-password', 'autofocus': True}),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'class': "form-control", 'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': "form-control", 'autocomplete': 'new-password'}),
    )
    captcha = CaptchaField(widget=CustomCaptchaTextInput(attrs={'class': "form-control"}))


class MySetPasswordForm(SetPasswordForm):
    captcha = CaptchaField(widget=CustomCaptchaTextInput(attrs={'class': "form-control"}))
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'class': "form-control", 'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': "form-control", 'autocomplete': 'new-password'}),
    )


class UserRegisterForm(UserCreationForm):
    captcha = CaptchaField(widget=CustomCaptchaTextInput(attrs={'class': "form-control"}))
    username = UsernameField(
        label=_("username"),
        widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete': 'off'})
    )

    first_name = forms.CharField(
        label=_("first name"),
        widget=forms.TextInput(attrs={'autofocus': True, 'class': "form-control", 'autocomplete': 'off'}),
        strip=True,
        help_text="",
        required=False,
    )

    last_name = forms.CharField(
        label=_("last name"),
        widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete': 'off'}),
        strip=True,
        help_text="",
        required=False,
    )

    mobile = forms.CharField(
        label=_("mobile"),
        widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete': 'off'}),
        help_text="",
    )

    phone = forms.CharField(
        label=_("phone"),
        widget=forms.TextInput(attrs={'class': "form-control", 'autocomplete': 'off'}),
        help_text="",
        required=False,
    )

    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'class': "form-control", 'autocomplete': 'off'})
    )

    # password1 = forms.CharField(
    #     label=_("New password"),
    #     widget=forms.PasswordInput(attrs={'class': "form-control", 'autocomplete': 'new-password'}),
    #     strip=False,
    #     help_text=password_validation.password_validators_help_text_html(),
    # )
    # password2 = forms.CharField(
    #     label=_("New password confirmation"),
    #     strip=False,
    #     widget=forms.PasswordInput(attrs={'class': "form-control", 'autocomplete': 'new-password'}),
    # )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': "form-control", 'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class': "form-control", 'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    address = forms.CharField(
        label=_("Address"),
        widget=forms.Textarea(attrs={'class': "form-control", 'rows': '4'}),
        strip=True,
        help_text="",
        required=False,
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = UserProfile
        fields = ['address', 'first_name', 'last_name', 'address', 'mobile', 'phone', 'username', 'email',
                  'password1',
                  'password2']
