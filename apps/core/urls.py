from django.urls import path, include

from .views import Home, AboutUs, Rules

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('about_us/', AboutUs.as_view(), name='about_us'),
    path('rules/', Rules.as_view(), name='rules'),
    path('ckeditor/', include('ckeditor_uploader.urls')),

]
