from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.functions import send_sms
from ..account.models import UserProfile


@receiver(post_save, sender=UserProfile)
def send_greeting_message(sender: AbstractUser, instance: UserProfile, created: bool, **kwargs):
    if created:
        message = f"{instance.username} عزیز عضویت تان در مجموعه آراد مهاجر را خوش آمد می گوییم."
        print(message)
        send_sms.delay(message, instance.mobile)
