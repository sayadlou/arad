# Generated by Django 3.2.12 on 2022-04-08 13:27

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_alter_event_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='policy',
            field=tinymce.models.HTMLField(default=''),
            preserve_default=False,
        ),
    ]
