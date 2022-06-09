# Generated by Django 3.2.13 on 2022-06-09 07:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_remove_userprofile_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='telegram_id',
            field=models.CharField(blank=True, max_length=100, null=True, validators=[django.core.validators.RegexValidator(message='Telegram ID باید با @ شروع شود', regex='^@')], verbose_name='Telegram ID'),
        ),
    ]