from django.utils import timezone
from rest_framework.test import APITestCase

from newslettersapp.models import Newsletter
from tags.models import Tag


class TestTagViewSet(APITestCase):
    def setUp(self) -> None:
        self.url_base = 'http://127.0.0.1:8000/api/v1'
        self.tag = Tag.objects.create(name='Tecnologia', slug='tecnologia')
        self.newsletter_1 = Newsletter.objects.create(
            name='Python', description='123', image='123', meta=100, target=0, frequency='123', tag=self.tag,
            created_at=timezone.now())
        self.newsletter_2 = Newsletter.objects.create(
            name='Python2', description='123', image='123', meta=100, target=0, frequency='123', tag=self.tag,
            created_at=timezone.now())

    def test_newsletters_action(self):
        url = f'{self.url_base}/tags/{self.tag.slug}/newsletters/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
