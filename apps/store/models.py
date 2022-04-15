from datetime import date
from uuid import uuid4

from azbankgateways.models import Bank
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from tinymce.models import HTMLField
from django_jalali.db import models as jmodels

from apps.account.models import UserProfile
from config.settings.base import product_models, learning_attachments_path


class ProductBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    max_order_quantity = models.DecimalField(max_digits=12, decimal_places=0)
    min_order_quantity = models.DecimalField(max_digits=12, decimal_places=0)
    purchaser = models.ManyToManyField(UserProfile, blank=True)

    def __str__(self):
        return f"{self.title}"

    def add_buyer(self, user):
        self.purchaser.add(user)

    def get_child(self):
        for attr in product_models:
            if getattr(self, attr, False):
                return getattr(self, attr)


class Cart(models.Model):
    CART_STATUS_WAITING = 'W'
    CART_STATUS_TRANSFERRED = 'T'
    CART_STATUS_FAILED = 'F'
    CART_STATUS_CHOICES = [
        (CART_STATUS_WAITING, 'Pending'),
        (CART_STATUS_TRANSFERRED, 'Transferred'),
        (CART_STATUS_FAILED, 'Failed')
    ]
    owner = models.OneToOneField(UserProfile, on_delete=models.RESTRICT)
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=CART_STATUS_CHOICES, max_length=20, default=CART_STATUS_WAITING)
    status_change_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')
        ordering = ('id',)

    def __str__(self):
        return self.owner.username


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('cart'), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    product = models.ForeignKey(ProductBaseModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Cart item')
        verbose_name_plural = _('Cart items')
        ordering = ('id',)

    def __str__(self):
        return f'{self.quantity} of {self.product.title}'

    class Meta:
        verbose_name = _('Cart item')
        verbose_name_plural = _('Cart items')
        ordering = ('id',)


class Order(models.Model):
    ORDER_STATUS_WAITING = 'W'
    ORDER_STATUS_TRANSFERRED = 'T'
    ORDER_STATUS_PAYED = 'P'
    ORDER_STATUS_FAILED = 'F'
    ORDER_STATUS_CHOICES = [
        (ORDER_STATUS_WAITING, 'Waiting'),
        (ORDER_STATUS_TRANSFERRED, 'Transferred'),
        (ORDER_STATUS_PAYED, 'Payed'),
        (ORDER_STATUS_FAILED, 'Failed')
    ]

    owner = models.ForeignKey(UserProfile, on_delete=models.RESTRICT)
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=ORDER_STATUS_CHOICES, max_length=20, default=ORDER_STATUS_WAITING)

    status_change_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Order')
        ordering = ('id',)

    @property
    def total_price(self):
        sum = 0
        for item in self.orderitem_set.all():
            sum += item.product.price * item.quantity
        return sum

    def __str__(self):
        return f"order of {self.owner.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name=_('order item'), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    product = models.ForeignKey(ProductBaseModel, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.quantity} of {self.product.title}'

    class Meta:
        verbose_name = _('Order item')
        verbose_name_plural = _('Order items')
        ordering = ('id',)

    @property
    def total_price(self):
        return self.quantity * self.product.price


class Payment(models.Model):
    STATUS_INITIAL = 1
    STATUS_PROCESSING = 2
    STATUS_CONFIRMED = 3
    STATUS_TYPE_CHOICES = [
        (STATUS_INITIAL, _('initial')),
        (STATUS_PROCESSING, _('processing')),
        (STATUS_CONFIRMED, _('confirmed')),
    ]
    owner = models.ForeignKey(UserProfile, on_delete=models.RESTRICT)
    order = models.ForeignKey(Order, verbose_name=_('order'), on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    expired_at = models.DateTimeField(verbose_name=_('expired at'), null=True, blank=True)
    due_at = models.DateTimeField(verbose_name=_('due at'), null=True, blank=True)
    fulfilled_at = models.DateTimeField(verbose_name=_('fulfilled at'), null=True, blank=True)
    amount = models.PositiveIntegerField(default=0, verbose_name=_('amount'))
    status = models.PositiveSmallIntegerField(verbose_name=_('status'), choices=STATUS_TYPE_CHOICES,
                                              default=STATUS_PROCESSING)
    status_change_date = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    transaction = GenericForeignKey('content_type', 'object_id')


class ServiceCategory(MPTTModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']


class Service(ProductBaseModel):
    STATUS = (
        ('Published', 'Published'),
        ('Draft', 'Draft'),
        ('Trash', 'Trash')
        ,
    )

    status = models.CharField(max_length=50, choices=STATUS)
    pub_date = jmodels.jDateTimeField(_("Date"))
    picture = models.ImageField(upload_to='event/picture')
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    seo_tag = models.CharField(max_length=200)
    description = HTMLField()
    introduction = HTMLField()

    def get_absolute_url(self):
        return reverse('store:service_slug', kwargs={'slug': self.slug})


class LearningCategory(MPTTModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']


class LearningPost(ProductBaseModel):
    STATUS = (
        ('Published', 'Published'),
        ('Draft', 'Draft'),
        ('Trash', 'Trash'),
    )

    content = HTMLField()
    introduction = HTMLField()
    status = models.CharField(max_length=50, choices=STATUS)
    view = models.BigIntegerField(null=True, blank=True, default=0)
    tags = models.CharField(max_length=200)
    pub_date = models.DateField(_("Date"), default=date.today)
    picture = models.ImageField(upload_to='learning/picture')
    category = models.ForeignKey(LearningCategory, on_delete=models.SET_NULL, null=True)
    video = models.ForeignKey('VideoFile', on_delete=models.CASCADE, null=True, blank=True)
    attachment = models.FileField(null=True, blank=True, storage=learning_attachments_path)

    def get_absolute_url(self):
        return reverse('store:learning_slug', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.title}'

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
        posts_tag = LearningPost.objects.values_list('tags')
        for post_tag in posts_tag:
            for tag in post_tag[0].split(','):
                if tag:
                    tag = clean_tag(tag)
                    tag_to_set.add(tag)
        return tag_to_set


class VideoFile(models.Model):
    name = models.CharField(max_length=255)
    arvan_id = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


class EventCategory(MPTTModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']


class Event(ProductBaseModel):
    STATUS = (
        ('Published', 'Published'),
        ('Draft', 'Draft'),
        ('Trash', 'Trash')
        ,
    )

    status = models.CharField(max_length=50, choices=STATUS)
    pub_date = jmodels.jDateTimeField(_("Date"))
    picture = models.ImageField(upload_to='event/picture')
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    seo_tag = models.CharField(max_length=200)
    start_date = jmodels.jDateTimeField()
    end_date = jmodels.jDateTimeField()
    duration = models.IntegerField()
    join_link = models.URLField(max_length=128)
    description = HTMLField()
    policy = HTMLField()
    organizer_mobile_number = models.CharField(_('mobile'), max_length=20, default=_('00989354356804'))

    def get_absolute_url(self):
        return reverse('store:event_slug', kwargs={'slug': self.slug})
