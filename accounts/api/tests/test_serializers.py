from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from accounts.api.serializer import UserModelSerializer


class UserModelSerializerApiTestCase(APITestCase):
    def setUp(self):
        self.UserModel = get_user_model()
        self.test_user = self.UserModel(email="test_email@gmail.com")
        self.test_user.set_password('1234')
        self.test_user.save()

    def test_serializer_with_valid_data(self):
        serializer = UserModelSerializer(data={
            'email': 'new_user@gmail.com',
            'password': "1234"
        })
        self.assertTrue(serializer.is_valid())

    def test_serializer_with_email_already_exist(self):
        serializer = UserModelSerializer(data={
            'email': self.test_user.email,
            'password': "1234"
        })
        self.assertFalse(serializer.is_valid())
