from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

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
            'personal_web_site': "در صورتی که فعالیت های آکادمیک یا تخصصی خود را در سایت خاصی پیاده سازی کرده اید آدرس آن را وارد کنید.",
            'linkedin_profile': "",
            'resume': "شما می توانید رزومه خود را با فرمت pdf و یا docx در اینجا آپلود فرماییدحداکثر حجم فایل: ۲۰۴۸kb",
            'gender': "",
            'marital_status': "",
            'education_status': "",
            'university': "",
            'field_of_study': "",
            'research_activity': "لطفا مقالات ژورنال و کنفرانسی خود را ذکر کنید.",
            'work_experience': "اگر تا کنون در مجموعه ای متناسب با رشته خود فعالیت انجام داده اید شرح دهید",
            'certificate': "هر کدام را با سال آن ذکر نمایید",
            'language_exam': "مدرک زبان بین المللی دارید؟",
            'language_exam_description': "",
            'destination_countries': "",
            'capital_for_immigration': "",
            'preference_to_join': "",
            'final_description': "",
        }

        labels = {
            'first_name': "نام ",
            'last_name': "نام خانوادگی ",
            'email': "پست الکترونیک شما ",
            'phone': "تلفن تماس شما ",
            'personal_web_site': "وبسایت شخصی یا کاری دارید؟",
            'linkedin_profile': "لینک پروفایل Linkedin شما",
            'resume': "آپلود رزومه (CV)",
            'gender': "جنسیت ",
            'marital_status': "وضعیت تاهل ",
            'education_status': "تحصیلات ",
            'university': "نام دانشگاه ",
            'field_of_study': "رشته تحصیلی ",
            'research_activity': "فعالیت های پژوهشی انجام دادید؟",
            'work_experience': "سوابق کارهای مرتبط با رشته",
            'certificate': "مدارک (Certification) و دوره های آموزشی انجام شده و اخذ شده",
            'language_exam': "آزمون زبان ",
            'language_exam_description': "توضیحات تکمیلی و دقیق در مورد وضعیت زبان و آمادگی برای آزمون را هم بفرمایید؟ ",
            'destination_countries': "کشورهای مقصد شما برای مهاجرت کجا هست؟",
            'capital_for_immigration': "سرمایه شما برای مهاجرت چند میلیون هست؟",
            'preference_to_join': "چرا دوست دارید که به تیم ما بپیوندید؟",
            'final_description': "توضیحات تکمیلی",
        }

    def save(self, commit=True):
        message = super().save(commit=False)

        if commit:
            message.save()
        return message
