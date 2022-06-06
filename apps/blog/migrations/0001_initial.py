# Generated by Django 3.2.13 on 2022-06-05 05:42

import ckeditor_uploader.fields
import datetime
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='blog.category')),
            ],
            options={
                'verbose_name': 'Blog Category',
                'verbose_name_plural': 'Blog Categories',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(allow_unicode=True, blank=True, max_length=200, primary_key=True, serialize=False, unique=True)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('status', models.CharField(choices=[('Published', 'Published'), ('Draft', 'Draft'), ('Trash', 'Trash')], max_length=50)),
                ('view', models.BigIntegerField(blank=True, default=0, null=True)),
                ('pub_date', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('picture', models.ImageField(upload_to='blog')),
                ('intro', models.TextField(max_length=500)),
                ('show_in_home', models.BooleanField(default=False)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.category')),
            ],
            options={
                'verbose_name': 'Blog Post',
                'verbose_name_plural': 'Blog Posts',
            },
        ),
    ]
