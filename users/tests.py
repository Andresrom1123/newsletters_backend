from django.utils import timezone
from rest_framework.test import APITestCase

from newslettersapp.models import Newsletter
from tags.models import Tag
from users.models import CustomUser


class TestUserViewSet(APITestCase):
    def setUp(self) -> None:
        self.url_base = 'http://127.0.0.1:8000/api/v1/users/'
        self.user = CustomUser.objects.create(email='prueba@123.com', first_name='Prueba', last_name='123',
                                              password='123')
        self.tag = Tag.objects.create(name='Prueba', slug='prueba')
        self.newsletter = Newsletter.objects.create(
            name='Boletin 1', description='123', image='123', target=0, frequency='Dy', author=self.user,
            created_at=timezone.now(), tag=self.tag, id=1)

    def test_author_action(self):
        url = f'{self.url_base}{self.user.id}/author/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_vote_action(self):
        url = f'{self.url_base}{self.user.id}/vote/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_subscribed_action(self):
        url = f'{self.url_base}{self.user.id}/subscribed/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
