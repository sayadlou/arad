from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, AbstractUser
from uuid import uuid4



class UserProfileManager(UserManager):
    pass


class UserProfile(AbstractUser):
    objects = UserProfileManager()

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    profile_picture = models.ImageField(_('profile picture'), upload_to='profile_pic', default='default_profile.png')
    address = models.TextField(_('address'), max_length=250, default=_('your address'))
    mobile = models.CharField(_('mobile'), max_length=20, default=_('00989123456789'))
    phone = models.CharField(_('phone'), max_length=20, default=_('00982112345678'))
