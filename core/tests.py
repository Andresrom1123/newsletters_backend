from rest_framework.test import APITestCase


class TestMyTokenObtainPairView(APITestCase):
    def setUp(self) -> None:
        self.url_base = 'http://127.0.0.1:8000/'
        self.url_user = f'{self.url_base}api/v1/users/'
        user = self.client.post(self.url_user, {'first_name': 'prueba', 'last_name': '123',
                                                'email': 'prueba@5.com', 'password': '123'})
        self.url_validate = f'{self.url_base}activate/{user.data["token"]}'
        self.response_validate = self.client.post(self.url_validate)

    def test_validate_email(self):
        self.assertEqual(self.response_validate.status_code, 200)

    def test_validate_data_token(self):
        url = f'{self.url_base}api/token/'
        response = self.client.post(url, {'email': 'prueba@5.com', 'password': '123'})
        self.assertEqual(response.data['first_name'], 'prueba')
        self.assertEqual(response.data['last_name'], '123')
        self.assertEqual(response.data['email'], 'prueba@5.com')
        self.assertEqual(response.data['is_staff'], False)
        self.assertEqual(response.data['is_admin'], False)
        self.assertEqual(response.data['id'], 1)
