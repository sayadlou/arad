import datetime
from uuid import uuid4

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from filer.fields.image import FilerImageField
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Blog Category')
        verbose_name_plural = _('Blog Categories')

    class MPTTMeta:
        order_insertion_by = ['name']


class Post(models.Model):
    STATUS = (
        ('Published', 'Published'),
        ('Draft', 'Draft'),
        ('Trash', 'Trash'),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(primary_key=True, max_length=200, unique=True, allow_unicode=True, blank=True)
    content = RichTextUploadingField()
    status = models.CharField(max_length=50, choices=STATUS)
    view = models.BigIntegerField(null=True, blank=True, default=0)
    pub_date = models.DateField(_("Date"), default=datetime.date.today)
    picture = FilerImageField(related_name='blog', on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    intro = models.TextField(max_length=500)
    show_in_home = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Blog Post')
        verbose_name_plural = _('Blog Posts')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:slug', kwargs={'slug': self.slug})

    @property
    def post_tags_list(self):
        tag_to_list = list()
        if "," in self.tags:
            tag_to_list = [x.strip() for x in self.tags.split(',')]
        else:
            tag_to_list.append(self.tags)
        return tag_to_list

    @staticmethod
    def blog_tags_list():
        def clean_tag(uncleaned_tag):
            cleaned_tag = str(uncleaned_tag)
            cleaned_tag = cleaned_tag.lower()
            cleaned_tag = cleaned_tag.strip()
            return cleaned_tag

        tag_to_set = set()
        posts_tag = Post.objects.values_list('tags')
        for post_tag in posts_tag:
            for tag in post_tag[0].split(','):
                if tag:
                    tag = clean_tag(tag)
                    tag_to_set.add(tag)
        return tag_to_set
