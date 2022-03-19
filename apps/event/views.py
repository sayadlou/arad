import os
from datetime import datetime, timedelta
from time import mktime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from .models import Event
from .permitions import BoughtUserMixin
from ..store.forms import CartItemForm


class IndexView(ListView):
    model = Event
    template_name = 'event/index.html'
    paginate_by = 6

    # all_posts = Post.objects.order_by('pub_date').filter(status='Published')

    def get_queryset(self):
        return self.model.objects.order_by('pub_date').filter(status='Published')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['model'] = ContentType.objects.get_for_model(Event).pk
        data['formmy'] = CartItemForm()

        return data


class SlugView(LoginRequiredMixin, DetailView):
    template_name = 'event/slug.html'
    model = Event


class CategoryView(ListView):
    model = Event
    template_name = 'learning/category.html'
    paginate_by = 6

    def get_queryset(self):
        category = self.kwargs['category']
        return self.model.objects.order_by('pub_date').filter(category__name__iexact=category)
