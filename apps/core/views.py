from django.views.generic import TemplateView

from apps.blog.models import Post as BlogPost


class Home(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["slides"] = BlogPost.objects.filter(show_in_home=True)
        return context


# Create your views here.
class AboutUs(TemplateView):
    template_name = 'core/about_us.html'

    def get_context_data(self, **kwargs):
        pass
