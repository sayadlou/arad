from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Post, Category


class Blog(ListView):
    template_name = 'blog/index.html'
    model = Post
    paginate_by = 6

    # all_posts = Post.objects.order_by('pub_date').filter(status='Published')

    def get_queryset(self):
        return self.model.objects.order_by('pub_date').filter(status='Published')


class Tag(ListView):
    template_name = 'blog/tag.html'
    model = Post
    paginate_by = 6

    def get_queryset(self):
        tag = self.request.GET.get("tag", "")
        return self.model.objects.order_by('pub_date').filter(status='Published').filter(tags__icontains=tag)


class Slug(DetailView):
    template_name = 'blog/slug.html'
    model = Post


class CategoryList(ListView):
    template_name = 'blog/category.html'
    model = Post
    paginate_by = 6

    def get_queryset(self):
        category = self.kwargs['category']
        return self.model.objects.order_by('pub_date').filter(category__name__iexact=category)
