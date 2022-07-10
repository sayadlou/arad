from django.urls import path
from django.views.generic import TemplateView

from .views import *

urlpatterns = [
    path('', ContactUs.as_view(), name='form'),
    path('thanks/', TemplateView.as_view(template_name="contact_us/thanks.html"), name='thanks'),
]
