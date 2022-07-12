from django.core.files import File
from django.test import TestCase
from django.urls import reverse

from ..models import *

from mock import MagicMock


class ViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_category1 = Category.objects.create(name="Man")
        test_category2 = Category.objects.create(name="Ali", parent=test_category1)
        file_mock = MagicMock(spec=File, name='FileMock')
        file_mock.name = 'test1.jpg'
        Post.objects.create(
            slug="test_slug",
            title="test_title",
            content="test_content",
            status="Published",
            view=10,
            picture=file_mock,
            tags="{Sport,Life}",
            category=test_category1,
        )
        Post.objects.create(
            slug="test_slug2",
            title="test_title2",
            content="test_content2",
            status="Draft",
            view=10,
            picture=file_mock,
            tags="{Car,Motor}",
            category=test_category2,
        )

    def test_index_page(self):
        response = self.client.get(reverse('blog:home'))
        self.assertEqual(response.status_code, 200)

    def test_tag_page(self):
        response = self.client.get(f"{reverse('blog:tag')}?tag=Sport")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f"{reverse('blog:tag')}?tag=SpOrT")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f"{reverse('blog:tag')}?tag=")
        self.assertEqual(response.status_code, 200)

    def test_post_page(self):
        page_pk = Post.objects.last().pk
        response = self.client.get(reverse('blog:post', kwargs={'pk': page_pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/service_slug.html')

    def test_slug_page(self):
        page_slug = Post.objects.last().slug
        response = self.client.get(reverse('blog:slug', kwargs={'slug': page_slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/service_slug.html')

    def test_category_page(self):
        page_category = Post.objects.last().category.name
        response = self.client.get(reverse('blog:category', kwargs={'category': page_category}))
        self.assertEqual(response.status_code, 200)
