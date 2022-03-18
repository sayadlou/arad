import datetime
from uuid import uuid4

from ckeditor_uploader.fields import RichTextUploadingField
from django.core.files.storage import FileSystemStorage
from django.contrib.postgres.fields import ArrayField, CICharField
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from ..account.models import UserProfile
from ..blog.models import Category as BlogCategory
from config.settings.base import learning_attachments_path

from ..store.models import Product as ProductBaseModel


class Category(MPTTModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']


class Post(ProductBaseModel):
    STATUS = (
        ('Published', 'Published'),
        ('Draft', 'Draft'),
        ('Trash', 'Trash'),
    )

    content = RichTextUploadingField()
    status = models.CharField(max_length=50, choices=STATUS)
    view = models.BigIntegerField(null=True, blank=True, default=0)
    tags = models.CharField(max_length=200)
    pub_date = models.DateField(_("Date"), default=datetime.date.today)
    picture = models.ImageField(upload_to='learning/picture')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    video = models.ForeignKey('VideoFile', on_delete=models.CASCADE, null=True, blank=True)
    attachment = models.FileField(null=True, blank=True, storage=learning_attachments_path)

    def get_absolute_url(self):
        return reverse('learning:slug', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.title}'

    @property
    def tags_list(self):
        tag_to_list = list()
        if "," in self.tags:
            tag_to_list = [x.strip() for x in self.tags.split(',')]
        else:
            tag_to_list.append(self.tags)
        return tag_to_list


class VideoFile(models.Model):
    name = models.CharField(max_length=255)
    arvan_id = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'
