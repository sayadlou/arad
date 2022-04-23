from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Post, Category


class Blog(ListView):
    template_name = 'blog/index.html'
    model = Post
    paginate_by = 6

    def get_queryset(self):
        return self.model.objects.order_by('pub_date').filter(status='Published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Post.blog_tags_list()
        return context


class Tag(ListView):
    template_name = 'blog/tag.html'
    model = Post
    paginate_by = 6

    def get_queryset(self):
        tag = str(self.request.GET.get("tag", "")).lower()
        print(self.model.blog_tags_list())
        if tag in self.model.blog_tags_list():
            return self.model.objects.order_by('pub_date').filter(status='Published').filter(tags__icontains=tag)
        return self.model.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Post.blog_tags_list()
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = self.kwargs.get('category')
        context['categories'] = Category.objects.all()
        context['tags'] = Post.blog_tags_list()
        return context
