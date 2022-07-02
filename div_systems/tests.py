import tempfile

from django.contrib.auth import get_user_model
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

# create image template
image = Image.new('RGB', (200, 200))
tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
image.save(tmp_file)
tmp_file.seek(0)

User = get_user_model()


class SignUpTests(APITestCase):

    def test_success(self):

        data = {
            'first_name': 'Ahmed',
            'last_name': 'Saied',
            'country_code': 'EG',
            'phone_number': '01221015107',
            'gender': 'male',
            'birthdate': '1995-01-01',
            'avatar': tmp_file,
            'email': 'ahmed.saied.dev@gmail.com',
            'password': 'ahmedsaid'
        }
        response = self.client.post('/signup/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UserViewsTests(APITestCase):
    # client = APIClient()

    def setUp(self):
        self.user = User.objects.create(
            first_name='ahmed',
            last_name='said',
            country_code='EG',
            phone_number='+201158626091',
            gender='male',
            birthdate='1995-01-01',
            email='ahmed.saeed311294@gmail.com',
        )
        self.user.set_password('ahmedahmed')
        self.user.save()
        refresh = RefreshToken.for_user(self.user)
        self.refresh = str(refresh)
        self.access = str(refresh.access_token)

    def test_login_success(self):
        response = self.client.post(
            '/login/', data={'phone_number': self.user.phone_number, 'password': 'ahmedahmed'})
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_login_password_error(self):
        response = self.client.post(
            '/login/', data={'phone_number': self.user.phone_number, 'password': 'ahmed'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_phone_error(self):
        response = self.client.post(
            '/login/', data={'phone_number': '4554545454', 'password': 'ahmed'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_status_is_authed(self):
        header = {'HTTP_AUTHORIZATION': 'Bearer '+self.access}
        response = self.client.get('/status/', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_status_is_un_authed(self):
        response = self.client.get('/status/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
