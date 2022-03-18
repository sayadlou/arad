from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Cart
from ..account.models import UserProfile


@receiver(post_save, sender=UserProfile)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(owner=instance)
