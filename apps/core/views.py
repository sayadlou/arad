from django.views.generic import TemplateView

from apps.blog.models import Post as BlogPost
from apps.store.models import LearningPost


class Home(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Posts"] = BlogPost.objects.filter(show_in_home=True)
        context["learnings"] = LearningPost.objects.filter(show_in_home=True)
        context["learnings_big"] = LearningPost.objects.filter(show_in_home=True, show_big_in_home=True)
        return context


class AboutUs(TemplateView):
    template_name = 'core/about_us.html'

    def get_context_data(self, **kwargs):
        pass


class Rules(TemplateView):
    template_name = 'core/rules.html'

    def get_context_data(self, **kwargs):
        pass
