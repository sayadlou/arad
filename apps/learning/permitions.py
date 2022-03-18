from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from .models import Post as LearningPost


class BoughtUserMixin(UserPassesTestMixin):
    raise_exception = False

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(f"{reverse_lazy('account:login')}?next={self.request.path}")
        return render(self.request, template_name="learning/pervent_message.html")

    def test_func(self):
        slug = self.kwargs.get(self.slug_url_kwarg)
        post = get_object_or_404(LearningPost, slug__iexact=slug)
        user_id = self.request.user.pk
        is_user_owner = post.purchaser.filter(pk=user_id).exists()
        if is_user_owner and self.request.user.is_authenticated:
            return True
        return False
