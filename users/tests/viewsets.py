from rest_framework.test import APITestCase
from users.models import CustomUser


class TestUserViewSet(APITestCase):

    def setUp(self) -> None:
        self.url_base = 'http://127.0.0.1:8000/'
        self.user = CustomUser.objects.create(email='prueba@123.com')
        self.user.set_password('1213')
        self.user.save()

    def test_validate_email(self):
        url = f'{self.url_base}activate/{self.user.token}'
        response_validate = self.client.post(url)
        self.assertEqual(response_validate.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.is_active, True)
