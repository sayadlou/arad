import datetime
from uuid import uuid4

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from ..store.models import Product as ProductBaseModel


class Category(MPTTModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']


class Organizer(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    mobile_number = models.CharField(_('mobile'), max_length=20, default=_('00989123456789'))
    policy = models.CharField(max_length=200)
    event = models.ForeignKey('Event', on_delete=models.RESTRICT, null=True)


class Event(ProductBaseModel):
    STATUS = (
        ('Published', 'Published'),
        ('Draft', 'Draft'),
        ('Trash', 'Trash'),
    )

    status = models.CharField(max_length=50, choices=STATUS)
    pub_date = models.DateField(_("Date"), default=datetime.date.today)
    picture = models.ImageField(upload_to='event/picture')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seo_tag = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    duration = models.IntegerField()
    join_link = models.URLField(max_length=128)
    description = models.TextField(max_length=400)

    def get_absolute_url(self):
        return reverse('event:slug', kwargs={'slug': self.slug})
