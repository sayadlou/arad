# Generated by Django 3.2.12 on 2022-04-02 12:54

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_post_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content2',
            field=tinymce.models.HTMLField(default=''),
            preserve_default=False,
        ),
    ]
