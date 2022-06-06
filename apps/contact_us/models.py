from uuid import uuid4

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Message(models.Model):
    checked_type = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    gender_choices = (
        ('male', _('Male')),
        ('female', _('Female')),
    )
    marital_choices = (
        ('single', _('Single')),
        ('married', _('Married')),
    )
    education_choices = (
        ("high_school", _('High school')),
        ("diploma", _('Diploma')),
        ("associate_degree", _('Associate Degree')),
        ("bachelor's_degree", _("Bachelor's degree")),
        ("master's_degree", _("Master's degree")),
        ("p.h.d", _('P.H.D')),
    )
    exam_choices = (
        ('ielts', _('IELTS')),
        ('toefl', _('TOEFL')),
        ('gre', _('GRE')),
        ('gmat', _('GMAT')),
        ('others', _('others')),
    )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    personal_web_site = models.URLField(null=True, blank=True)
    linkedin_profile = models.URLField(null=True, blank=True)
    resume = models.FileField(null=True, blank=True)
    gender = models.CharField(max_length=50, choices=gender_choices)
    marital_status = models.CharField(max_length=50, choices=gender_choices)
    education_status = models.CharField(max_length=50, choices=gender_choices)
    university = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    research_activity = models.TextField(max_length=1000, null=True, blank=True)
    work_experience = models.TextField(max_length=1000, null=True, blank=True)
    certificate = models.TextField(max_length=1000, null=True, blank=True)
    language_exam = models.CharField(max_length=50, choices=exam_choices)
    language_exam_description = models.TextField(max_length=1000)
    destination_countries = models.CharField(max_length=100)
    capital_for_immigration = models.CharField(max_length=100, null=True, blank=True)
    preference_to_join = models.TextField(max_length=1000)
    final_description = models.TextField(max_length=1000)
    submission_time = models.DateTimeField(auto_now_add=True, editable=True)

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
