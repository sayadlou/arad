# Generated by Django 3.2.12 on 2022-05-24 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20220524_1806'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='content3',
            new_name='content',
        ),
    ]