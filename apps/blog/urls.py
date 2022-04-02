from django.urls import path

from .views import Blog,  Slug, Tag, CategoryList

urlpatterns = [
    path('', Blog.as_view(), name='home'),
    path('tag/', Tag.as_view(), name='tag'),
    path('post/<str:slug>', Slug.as_view(), name='slug'),
    path('category/<str:category>', CategoryList.as_view(), name='category'),
]
