from django.urls import path, re_path

from .views import SlugView, TagView, CategoryView, IndexView, AttachmentView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('post/<slug:slug>', SlugView.as_view(), name='slug'),
    path('tag/', TagView.as_view(), name='tag'),
    path('category/<str:category>', CategoryView.as_view(), name='category'),
    re_path(r"^attachment/(?P<slug>[a-zA-Z0-9_-]+)/$", AttachmentView.as_view(), name='attachment')
]
