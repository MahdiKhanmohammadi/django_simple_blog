from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_405_METHOD_NOT_ALLOWED, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework.test import APIClient


class RegisterApiTestCase(APITestCase):
    def setUp(self):
        self.UserModel = get_user_model()
        self.path = "/account/register/"
        self.test_data_for_user = {
            'email': 'test_email@gmail.com',
            'password': '1234'
        }

    def test_invalid_get_method(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_method_is_valid_and_create_user(self):
        response = self.client.post(
            self.path, data=self.test_data_for_user)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertTrue(self.UserModel.objects.filter(
            email=self.test_data_for_user.get('email')).exists())


class ActiveAccountApiTestCase(APITestCase):
    def setUp(self):
        self.path = "/account/active/"
        self.UserModel = get_user_model()
        self.test_user = self.UserModel(
            email='test_user@gmail.com')
        self.test_user.set_password("1234")
        self.test_user.save()

    def test_active_account_valid_user(self):
        path = self.path+f"{self.test_user.verify_code}/"
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTP_200_OK)
        get_user = self.UserModel.objects.get(pk=self.test_user.pk)
        self.assertTrue(get_user.is_active)

    def test_active_account_invalid_user(self):
        # test with verify code the does not exist
        path = self.path+"jcjoajoiasjiocjsoijicao/"
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)


class DestroyCurrentTokenApiViewTest(APITestCase):
    def setUp(self):
        self.UserModel = get_user_model()
        self.test_user = self.UserModel(
            email="test_email@gmail.com", is_active=True)
        self.test_user.set_password('1234')
        self.test_user.save()

        self.test_user_token = Token.objects.create(user=self.test_user)

        self.url_path = "account/destroy-token/"
        self.reverse_path = reverse('accounts_api:destroy_token')

    def test_destroy_token(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' +
                           self.test_user_token.key)
        response = client.get(self.reverse_path)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertFalse(Token.objects.filter(user=self.test_user).exists())
