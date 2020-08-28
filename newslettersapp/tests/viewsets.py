from django.utils import timezone
from rest_framework.test import APITestCase

from newslettersapp.models import Newsletter
from tags.models import Tag
from users.models import CustomUser


class TestNewsletterViewSet(APITestCase):
    def setUp(self) -> None:
        self.url_base = 'http://127.0.0.1:8000/api/v1/newsletters/'
        self.user_1 = CustomUser.objects.create(email='prueba@123.com', first_name='Prueba', last_name='123',
                                                password='123')
        self.tag = Tag.objects.create(name='123', slug='123')
        self.newsletter_1 = Newsletter.objects.create(
            name='Boletin 1', description='123', image='123', target=0, frequency='Dy', author=self.user_1,
            created_at=timezone.now(), tag=self.tag)

    def test_vote_get_action(self):
        url = f'{self.url_base}vote_get/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_subscribe_get_action(self):
        url = f'{self.url_base}subscribe_get/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
