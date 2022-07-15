from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserProfileManager(UserManager):
    pass


class UserProfile(AbstractUser):
    objects = UserProfileManager()

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    mobile = models.CharField(_('mobile'), max_length=20, validators=[
        RegexValidator(regex="^(?=.{11})09", message="شماره موبایل معتبر نیست")
    ])
    telegram_id = models.CharField(_('Telegram ID'), max_length=100, null=True, blank=True,
                                   validators=[RegexValidator(regex="^@", message="Telegram ID باید با @ شروع شود")])
