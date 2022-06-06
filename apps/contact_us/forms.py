from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from .models import Message

owner_email = (
    ('Department1@example.com', _('Department1')),
    ('Department2@example.com', _('Department2')),
    ('Department3@example.com', _('Department3')),
)


class ContactForm(ModelForm):
    class Meta:
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields:
                field.widget.attrs.update({'class': 'form-control'})
            self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
            self.fields['last_name'].widget.attrs.update({'class': 'form-control'})

        model = Message
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone',
            'personal_web_site',
            'linkedin_profile',
            'resume',
            'gender',
            'marital_status',
            'education_status',
            'university',
            'field_of_study',
            'research_activity',
            'work_experience',
            'certificate',
            'language_exam',
            'language_exam_description',
            'destination_countries',
            'capital_for_immigration',
            'preference_to_join',
            'final_description',
        )
        help_texts = {
            'personal_web_site':
                _("If you have implemented your academic or professional activities on a specific site, enter its address."),
            'linkedin_profile': "",
            'resume': "",
            'gender': "",
            'marital_status': "",
            'education_status': "",
            'university': "",
            'field_of_study': "",
            'research_activity': "",
            'work_experience': "",
            'certificate': "",
            'language_exam': "",
            'language_exam_description': "",
            'destination_countries': "",
            'capital_for_immigration': "",
            'preference_to_join': "",
            'final_description': "",
        }

        labels = {
            # 'first_name': "",
            # 'last_name': "",
            # 'email': "",
            # 'phone': "",
            # 'personal_web_site': "",
            # 'linkedin_profile': "",
            # 'resume': "",
            # 'gender': "",
            # 'marital_status': "",
            # 'education_status': "",
            # 'university': "",
            # 'field_of_study': "",
            # 'research_activity': "",
            # 'work_experience': "",
            # 'certificate': "",
            # 'language_exam': "",
            # 'language_exam_description': "",
            # 'destination_countries': "",
            # 'capital_for_immigration': "",
            # 'preference_to_join': "",
            # 'final_description': "",
        }

    def save(self, commit=True):
        message = super().save(commit=False)

        if commit:
            message.save()
        return message
