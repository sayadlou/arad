# Generated by Django 3.2.14 on 2022-07-18 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_service_picture_descrip'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service',
            old_name='picture_intro',
            new_name='picture',
        ),
    ]
