from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import *


# def contactus(request):
#     contact_form = ContactForm()
#     if request.POST:
#         contact_form = ContactForm(request.POST)
#         if contact_form.is_valid():
#             contact_form.save()
#             messages.info(request, 'your message has been seved')
#             contact_form = ContactForm()
#     context = {
#         'contact_form': contact_form,
#     }
#     return render(request, 'contact_us/form.html', context)


class ContactUs(CreateView):
    model = Message
    form_class = ContactForm
    success_url = reverse_lazy('contact_us:thanks')


