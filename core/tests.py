from rest_framework.test import APITestCase

from users.models import CustomUser


class TestMyTokenObtainPairView(APITestCase):

    def setUp(self) -> None:
        self.url_base = 'http://127.0.0.1:8000/'
        self.user = CustomUser.objects.create(email='prueba@123.com', first_name='prueba', last_name='123')
        self.user.set_password('123')
        self.user.is_active = True
        self.user.save()

    def test_validate_data_token(self):
        url = f'{self.url_base}api/token/'
        response = self.client.post(url, {'email': self.user.email, 'password': '123'})
        self.assertEqual(response.data['first_name'], 'prueba')
        self.assertEqual(response.data['last_name'], '123')
        self.assertEqual(response.data['email'], 'prueba@123.com')
        self.assertEqual(response.data['is_staff'], False)
        self.assertEqual(response.data['is_admin'], False)
        self.assertEqual(response.data['id'], 1)
