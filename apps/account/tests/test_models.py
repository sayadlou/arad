from django.test import TestCase
from ..models import *


class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up an objects used by all test methods
        UserProfile.objects.create(
            email="sample@gmail.com",
            username="saeid",
            address="iran tehran ",
            password="12345",
            first_name='saeid',
            last_name='sayadlou',
        )

    def test_get_full_name(self):
        user = UserProfile.objects.last()

        self.assertEqual(user.get_full_name(), 'saeid sayadlou')
        self.assertEqual(user.address, "iran tehran ")
