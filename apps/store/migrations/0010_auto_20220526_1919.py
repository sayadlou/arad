# Generated by Django 3.2.12 on 2022-05-26 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_auto_20220526_1918'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='picture2',
            new_name='picture',
        ),
        migrations.RenameField(
            model_name='learningpost',
            old_name='picture2',
            new_name='picture',
        ),
        migrations.RenameField(
            model_name='service',
            old_name='picture2',
            new_name='picture',
        ),
    ]