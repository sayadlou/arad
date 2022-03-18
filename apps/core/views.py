from django.views.generic import TemplateView, DetailView, ListView, FormView


class Home(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# Create your views here.
class AboutUs(TemplateView):
    template_name = 'core/about_us.html'

    def get_context_data(self, **kwargs):
        pass
