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
            'resume': _("You can upload your resume in pdf or docx format here Maximum file size: 2048kb"),
            'gender': "",
            'marital_status': "",
            'education_status': "",
            'university': "",
            'field_of_study': "",
            'research_activity': "Please cite your journal and conference papers.",
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
            'first_name': _("First Name"),
            'last_name': _("Last Name"),
            'email': _("Email"),
            'phone': _("Phone"),
            'personal_web_site': _("Personal Web Site"),
            'linkedin_profile': _("Linkedin Profile"),
            'resume': _("Resume"),
            'gender': _("Gender"),
            'marital_status': _("Marital Status"),
            'education_status': _("Education Status"),
            'university': _("University"),
            'field_of_study': _("Field Of Study"),
            'research_activity': _("Research Activity"),
            'work_experience': _("Work Experience"),
            'certificate': _("Certificate"),
            'language_exam': _("Language Exam"),
            'language_exam_description': _("Language Exam Description"),
            'destination_countries': _("Destination Countries"),
            'capital_for_immigration': _("Capital For Immigration"),
            'preference_to_join': _("Preference To Join"),
            'final_description': _("Final Description"),
        }

    def save(self, commit=True):
        message = super().save(commit=False)

        if commit:
            message.save()
        return message
