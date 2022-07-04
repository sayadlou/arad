from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from .views import Home, AboutUs, celery_test

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('about_us/', AboutUs.as_view(), name='about_us'),
    path('rules/', AboutUs.as_view(), name='rules'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('test/', celery_test, name='celery_test'),

]
