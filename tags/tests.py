from django.utils import timezone
from rest_framework.test import APITestCase

from newslettersapp.models import Newsletter
from tags.models import Tag
from users.models import CustomUser


class TestTagViewSet(APITestCase):
    def setUp(self) -> None:
        self.url_base = 'http://127.0.0.1:8000/api/'
        self.tag = Tag.objects.create(name='Tecnologia', slug='tecnologia')
        self.user = CustomUser.objects.create(email='prueba@123.com')
        self.user.set_password('123')
        self.user.is_active = True
        self.user.save()
        self.newsletter_1 = Newsletter.objects.create(
            name='Python', description='123', image='123', target=10, frequency='Dy', tag=self.tag,
            created_at=timezone.now(), author=self.user)
        self.newsletter_2 = Newsletter.objects.create(
            name='Python2', description='123', image='123', target=1, frequency='Dy', tag=self.tag,
            created_at=timezone.now(), author=self.user)
        self.token = self.client.post(f'{self.url_base}token/', {'email': self.user.email, 'password': '123'})

    def test_newsletters_vote_action(self):
        url = f'{self.url_base}v1/tags/{self.tag.slug}/newsletters_vote/'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.token.data["token"]}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_newsletters_subscribed_action(self):
        url = f'{self.url_base}v1/tags/{self.tag.slug}/newsletters_subscribed/'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.token.data["token"]}')
        self.assertEqual(response.status_code, 200)
