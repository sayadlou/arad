# Generated by Django 3.2.12 on 2022-05-24 13:03

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_post_content3'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content3',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
