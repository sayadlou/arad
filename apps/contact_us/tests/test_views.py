from django.test import TestCase
from django.urls import reverse

from ..models import Message


class ViewTest(TestCase):

    def test_thanks(self):
        response = self.client.get(reverse('contact_us:thanks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact_us/thanks.html')

    def test_form(self):
        response = self.client.get(reverse('contact_us:form'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact_us/message_form.html')

        my_data = {
            'subject': 'some message',
            'phone': 'saeid',
            'email': 'saeid@sef.csdf',
            'content': 'hi man',
            'captcha_0': 'dummy-value',
            'captcha_1': 'PASSED',
        }
        response = self.client.post(
            reverse('contact_us:form'),
            data=my_data
        )
        print(Message.objects.all().count())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Message.objects.all().count(), 1)
