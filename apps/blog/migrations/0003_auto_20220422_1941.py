# Generated by Django 3.2.12 on 2022-04-22 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20220415_2220'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Blog Category', 'verbose_name_plural': 'Blog Categories'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'Blog Post', 'verbose_name_plural': 'Blog Posts'},
        ),
    ]