import os
from pathlib import Path

from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load .env file

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = int(os.environ.get("DEBUG", 0))

# Application definition

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.humanize',
    'django.forms',
    'easy_thumbnails',
    'filer',
    'django_jalali',
    'captcha',
    'ckeditor',
    'ckeditor_uploader',
    'mptt',
    'dbbackup',
    'azbankgateways',
    'apps.core',
    'apps.blog',
    'apps.account',
    'apps.contact_us',
    'apps.store',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.core.middleware.RemoteAddrMiddleware'
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.cart_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'fa'

LANGUAGES = (
    ('en', _('English')),
    ('fa', _('Persian')),

)

LOCALE_PATHS = (
    BASE_DIR / 'locale/',
)

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "static"
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

ATTACHMENT_URL = '/attachment/'
ATTACHMENT_ROOT = BASE_DIR / "learning_attachments"

STATICFILES_DIRS = [
]

learning_attachments_path = FileSystemStorage(location=ATTACHMENT_ROOT, base_url=ATTACHMENT_URL)

AUTH_USER_MODEL = "account.UserProfile"

LOGIN_REDIRECT_URL = reverse_lazy('account:profile')
LOGIN_URL = reverse_lazy('account:login')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = BASE_DIR / "media/ckeditor"
CKEDITOR_FILENAME_GENERATOR = 'utils.functions.get_filename'

AZ_IRANIAN_BANK_GATEWAYS = {
    'GATEWAYS': {
        'ZARINPAL': {
            'MERCHANT_CODE': os.environ['ZARINPAL_MERCHANT_CODE'],
            'SANDBOX': int(os.environ['ZARINPAL_SANDBOX']),
        },
    },
    'DEFAULT': 'ZARINPAL',
    'CURRENCY': 'IRR',
    'TRACKING_CODE_QUERY_PARAM': 'tc',
    'TRACKING_CODE_LENGTH': 16,
}
MINIMUM_ORDER_AMOUNT = 100000
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/general.log',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO')
        }
    },
    'formatters': {
        'verbose': {
            'format': '{asctime} ({levelname}) - {name} - {message}',
            'style': '{'
        }
    }
}

product_models = [
    "learningpost",
    "service",
    "event",
]
ALLOW_UNICODE_SLUGS = True

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 900,
    },
}

CKEDITOR_BROWSE_SHOW_DIRS = True

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    # 'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': BASE_DIR / 'backup'}

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/1'

ARVAN_CHANNEL_ID = os.environ.get('ARVAN_CHANNEL_ID')
ARVAN_API_KEY = os.environ.get('ARVAN_API_KEY')
SMS_SENDER_NUMBER = os.environ.get('SMS_SENDER_NUMBER')
