from django.utils import timezone
from rest_framework.test import APITestCase

from newslettersapp.models import Newsletter
from tags.models import Tag
from users.models import CustomUser


class TestUserPermissions(APITestCase):

    def setUp(self) -> None:
        self.url_base = 'http://127.0.0.1:8000/api/'
        self.user = CustomUser.objects.create(email='prueba@123.com')
        self.user.set_password('123')
        self.user.is_active = True
        self.user.save()
        self.token = self.client.post(f'{self.url_base}token/', {'email': self.user.email, 'password': '123'})
        self.tag = Tag.objects.create(name='123', slug='123')
        self.newsletter = Newsletter.objects.create(
            name='Boletin 1', description='123', image='123', target=0, frequency='Dy', author=self.user,
            created_at=timezone.now(), tag=self.tag)
        self.newsletter_2 = Newsletter.objects.create(
            name='Boletin 2', description='123', image='123', target=10, frequency='Dy', author=self.user,
            created_at=timezone.now(), tag=self.tag)

    def test_no_staff_action(self):
        self.user.is_admin = True
        self.user.save()
        endpoint = f'{self.url_base}v1/users/no_staff/'
        response = self.client.get(endpoint, HTTP_AUTHORIZATION=f'Bearer {self.token.data["token"]}')
        self.assertEqual(response.status_code, 200)

    def test_no_staff_action_failed(self):
        endpoint = f'{self.url_base}v1/users/no_staff/'
        response = self.client.get(endpoint, HTTP_AUTHORIZATION=f'Bearer {self.token.data["token"]}')
        self.assertEqual(response.status_code, 403)

    def test_voted_action(self):
        self.newsletter_2.users.add(self.user)
        self.newsletter.save()
        endpoint = f'{self.url_base}v1/users/{self.user.id}/voted/'
        response = self.client.get(endpoint, HTTP_AUTHORIZATION=f'Bearer {self.token.data["token"]}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_subscribed_action(self):
        self.newsletter.users.add(self.user)
        self.newsletter.save()
        endpoint = f'{self.url_base}v1/users/{self.user.id}/subscribed/'
        response = self.client.get(endpoint, HTTP_AUTHORIZATION=f'Bearer {self.token.data["token"]}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_author_action(self):
        self.user.is_staff = True
        self.user.save()
        endpoint = f'{self.url_base}v1/users/{self.user.id}/author/'
        response = self.client.get(endpoint, HTTP_AUTHORIZATION=f'Bearer {self.token.data["token"]}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_author_action_failed(self):
        endpoint = f'{self.url_base}v1/users/{self.user.id}/author/'
        response = self.client.get(endpoint, HTTP_AUTHORIZATION=f'Bearer {self.token.data["token"]}')
        self.assertEqual(response.status_code, 403)

    def test_staff_action(self):
        user_2 = CustomUser.objects.create(email='amclres@gmail.com')
        user_2.set_password('1234')
        user_2.save()
        self.user.is_admin = True
        self.user.save()
        endpoint = f'{self.url_base}v1/users/staff/'
        data = {
            'user': user_2.id
        }
        response = self.client.post(endpoint, data=data, HTTP_AUTHORIZATION=f'Bearer {self.token.data["token"]}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user_2.is_staff, False)
        user_2.refresh_from_db()
        self.assert_(user_2.is_staff, True)

    def test_staff_action_failed(self):
        user_2 = CustomUser.objects.create(email='usuario_2@123.com', password='12345')
        user_2.is_staff = True
        user_2.save()
        self.user.is_admin = True
        self.user.save()
        endpoint = f'{self.url_base}v1/users/staff/'
        data = {
            'user': user_2.id
        }
        response = self.client.post(endpoint, data=data, HTTP_AUTHORIZATION=f'Bearer {self.token.data["token"]}')
        self.assertEqual(response.status_code, 400)
