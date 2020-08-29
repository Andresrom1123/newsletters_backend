from rest_framework.test import APITestCase
from users.models import CustomUser


class TestUserViewSet(APITestCase):

    def setUp(self) -> None:
        self.url_base = 'http://127.0.0.1:8000/'
        self.user = CustomUser.objects.create(email='amclres@gmail.com')
        self.user.set_password('1213')
        self.user.save()

    def test_validate_email(self):
        url = f'{self.url_base}api/v1/activate/{self.user.token}'
        response_validate = self.client.post(url)
        self.assertEqual(response_validate.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.is_active, True)

    def test_action_email_reset_password(self):
        url = f'{self.url_base}api/v1/users/email_reset_password/'
        data = {
            'email': self.user.email
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_reset_password(self):
        url = f'{self.url_base}api/v1/reset_password/{self.user.token}'
        data = {
            'password': 'prueba234'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
