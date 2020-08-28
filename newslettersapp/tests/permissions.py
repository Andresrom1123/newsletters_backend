from django.utils import timezone
from rest_framework.test import APITestCase

from newslettersapp.models import Newsletter
from tags.models import Tag
from users.models import CustomUser


class TesNewsletterPermissions(APITestCase):

    def setUp(self) -> None:
        self.url_base = 'http://127.0.0.1:8000/api/'
        self.user = CustomUser.objects.create(email='amclres@gmail.com')
        self.user.set_password('123')
        self.user.is_active = True
        self.user.save()
        self.t = Tag.objects.create(name='123', slug='123')
        self.n_1 = Newsletter.objects.create(
            name='Boletin 1', description='123', image='123', target=0, frequency='Dy', author=self.user,
            created_at=timezone.now(), tag=self.t)
        self.n_2 = Newsletter.objects.create(
            name='Boletin 2', description='123', image='123', subscribed=9, target=10, frequency='Dy', author=self.user,
            created_at=timezone.now(), tag=self.t)
        self.token = self.client.post(f'{self.url_base}token/', {'email': self.user.email, 'password': '123'})

    def test_subscribe_action(self):
        url = f'{self.url_base}v1/newsletters/{self.n_1.id}/subscribe/'
        data = {
            'user': self.user.id
        }
        response = self.client.post(url, data=data, HTTP_AUTHORIZATION=f'Bearer {self.token.data["token"]}')
        self.assertEqual(response.status_code, 200, 'Ha ocurrido un error')

    def test_subscribe_action_failed(self):
        url = f'{self.url_base}v1/newsletters/{self.n_1.id}/subscribe/'
        data = {
            'user': self.user.id
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 401, 'Ha ocurrido un error')

    def test_vote_action(self):
        url = f'{self.url_base}v1/newsletters/{self.n_2.id}/vote/'
        data = {
            'user': self.user.id
        }
        response = self.client.post(url, data=data, HTTP_AUTHORIZATION=f'Bearer {self.token.data["token"]}')
        self.assertEqual(response.status_code, 200, 'Ha ocurrido un error')
        self.n_2.refresh_from_db()
        self.assertEqual(self.n_2.subscribed, 10)

    def test_vote_action_failed(self):
        url = f'{self.url_base}v1/newsletters/{self.n_2.id}/vote/'
        data = {
            'user': self.user.id
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 401, 'Ha ocurrido un error')

    def test_destroy(self):
        self.user.is_staff = True
        self.user.save()
        url = f'{self.url_base}v1/newsletters/{self.n_1.id}/'
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {self.token.data["token"]}')
        self.assertEqual(response.status_code, 204, 'El usuario no es staff')

    def test_destroy_failed(self):
        url = f'{self.url_base}v1/newsletters/{self.n_1.id}/'
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {self.token.data["token"]}')
        self.assertEqual(response.status_code, 403, 'El usuario no es staff')
