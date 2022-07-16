from django.http import HttpResponse
from django.views.generic import TemplateView

from apps.blog.models import Post as BlogPost
from apps.account.tasks import send_sms
from apps.store.models import Event, Service


class Home(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Posts"] = BlogPost.objects.filter(show_in_home=True)
        context["events"] = Event.objects.filter(show_in_home=True)
        context["services"] = Service.objects.filter(show_in_home=True, highlight_in_home=False)
        context["highlight_services"] = Service.objects.filter(show_in_home=True, highlight_in_home=True)
        return context


class AboutUs(TemplateView):
    template_name = 'core/about_us.html'

    def get_context_data(self, **kwargs):
        pass


class Rules(TemplateView):
    template_name = 'core/rules.html'

    def get_context_data(self, **kwargs):
        pass


def celery_test(request):
    send_sms.delay("salam")
    return HttpResponse('result')
