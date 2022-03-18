from django.forms import ModelForm
from django import forms
from .models import Message
from captcha.fields import CaptchaField, CaptchaTextInput
from django.utils.translation import ugettext_lazy as _

from ..account.widget import CustomCaptchaTextInput

owner_email = (
    ('Department1@example.com', _('Department1')),
    ('Department2@example.com', _('Department2')),
    ('Department3@example.com', _('Department3')),
)


class ContactForm(ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'phone', 'email', 'content', 'captcha']

    subject = forms.CharField(
        label=_("Subject")
    )
    phone = forms.CharField(
        required=False,
        label=_('Phone number')
    )
    email = forms.EmailField(
        label=_('Email')
    )
    content = forms.CharField(
        widget=forms.Textarea,
        label=_('Message')
    )
    captcha = CaptchaField(widget=CustomCaptchaTextInput(attrs={'class': "form-control"}))
    subject.widget.attrs.update({'class': 'form-control', 'placeholder': _("Subject")})
    phone.widget.attrs.update({'class': 'form-control', 'placeholder': _('Phone number')})
    email.widget.attrs.update({'class': 'form-control', 'placeholder': _('Email')})
    content.widget.attrs.update({'class': 'form-control', 'placeholder': _('Message'), 'rows': '5'})

    def save(self, commit=True):
        message = super().save(commit=False)

        if commit:
            message.save()
        return message
