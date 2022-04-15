from django.urls import path, re_path

from .views import SlugView, CategoryView, IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('event/<slug:slug>', SlugView.as_view(), name='slug'),
    path('category/<str:category>', CategoryView.as_view(), name='category'),
]
