# Generated by Django 3.2.14 on 2022-09-30 15:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('phone', models.CharField(max_length=15)),
                ('personal_web_site', models.URLField(blank=True, null=True)),
                ('linkedin_profile', models.URLField(blank=True, null=True)),
                ('resume', models.FileField(blank=True, null=True, upload_to='')),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=50)),
                ('marital_status', models.CharField(choices=[('single', 'Single'), ('married', 'متاهل')], max_length=50)),
                ('education_status', models.CharField(choices=[('high_school', 'High school'), ('diploma', 'Diploma'), ('associate_degree', 'Associate Degree'), ("bachelor's_degree", "Bachelor's degree"), ("master's_degree", "Master's degree"), ('p.h.d', 'P.H.D')], max_length=50)),
                ('university', models.CharField(max_length=100)),
                ('field_of_study', models.CharField(max_length=100)),
                ('research_activity', models.TextField(blank=True, max_length=1000, null=True)),
                ('work_experience', models.TextField(blank=True, max_length=1000, null=True)),
                ('certificate', models.TextField(blank=True, max_length=1000, null=True)),
                ('language_exam', models.CharField(choices=[('ielts', 'IELTS'), ('toefl', 'TOEFL'), ('gre', 'GRE'), ('gmat', 'GMAT'), ('others', 'others')], max_length=50)),
                ('language_exam_description', models.TextField(blank=True, max_length=1000, null=True)),
                ('destination_countries', models.CharField(max_length=100)),
                ('capital_for_immigration', models.CharField(blank=True, max_length=100, null=True)),
                ('preference_to_join', models.TextField(blank=True, max_length=1000, null=True)),
                ('final_description', models.TextField(blank=True, max_length=1000, null=True)),
                ('submission_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
        ),
    ]
