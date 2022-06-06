from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import *


class ContactUs(CreateView):
    model = Message
    form_class = ContactForm
    success_url = reverse_lazy('contact_us:thanks')

    def get(self, request, *args, **kwargs):
        self.edit_form()
        return super().get(request, *args, **kwargs)

    def edit_form(self):
        for _, field in self.form_class.base_fields.items():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["oninput"] = "this.className = 'form-control '"
