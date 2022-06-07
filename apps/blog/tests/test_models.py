from django.test import TestCase
from ..models import *


class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up an objects used by all test methods
        test_category1 = Category.objects.create(name="Man")
        test_category2 = Category.objects.create(name="Ali", parent=test_category1)
        Post.objects.create(
            slug="test_slug",
            title="test_title",
            content="test_content",
            status="Published",
            view=10,
            tags="{Sport,Life}",
            category=test_category1,
        )
        Post.objects.create(
            slug="test_slug2",
            title="test_title2",
            content="test_content2",
            status="Draft",
            view=10,
            tags="{Car,Motor}",
            category=test_category2,
        )

    def test_category(self):
        self.assertEqual(Category.objects.all().count(), 2)

    def test_post(self):
        self.assertEqual(Post.objects.all().count(), 2)


    # def test_get_full_name(self):
    #     user = Category.objects.last()
    #
    #     self.assertEqual(user.get_full_name(), 'saeid sayadlou')
    #     self.assertEqual(user.address, "iran tehran ")
