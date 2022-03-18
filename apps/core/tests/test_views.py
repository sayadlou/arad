from django.test import TestCase
from django.urls import reverse


class ViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def test_home(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')

    def test_about_us(self):
        response = self.client.get(reverse('core:about_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/about_us.html')
