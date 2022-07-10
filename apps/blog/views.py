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
        return context
