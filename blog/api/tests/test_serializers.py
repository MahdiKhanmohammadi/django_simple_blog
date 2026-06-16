from django.test import SimpleTestCase, TestCase
from blog.api.serializer import CategoryModelSerializer, PostWriteModelSerializer
import datetime
from blog.models import Category
from django.contrib.auth import get_user_model


class CategorySerializerTest(SimpleTestCase):

    def setUp(self):
        self.serializer = CategoryModelSerializer

    def test_with_valid_data(self):
        data = {
            'title': "test_title",
            'status': 'True',
            'created_date': datetime.datetime.now()
        }

        self.assertTrue(self.serializer(data=data).is_valid())

    def test_with_invalid_data(self):
        data = {
            'title': 'test_title',
            'status': 'dfjsdjofsod',
            'created_date': datetime.datetime.now()
        }
        self.assertFalse(self.serializer(data=data).is_valid())


class PostSerializerTest(TestCase):

    def setUp(self):
        self.serializer = PostWriteModelSerializer
        User = get_user_model()
        self.category = Category.objects.create(title='test', status=True)
        self.user = User.objects.create(
            email='email@gmail.com', password="1234")

    def test_with_valid_data(self):
        data = {
            'title': "test_title",
            'status': 'True',
            'content': 'test content',
            'author': self.user.pk,
            'category': self.category.pk
        }
        self.assertTrue(self.serializer(data=data).is_valid())

    def test_with_invalid_data(self):
        data = {
            'title': 'test_title',
            'category': self.category.pk,
            'content': 'test-content'
        }
        self.assertFalse(self.serializer(data=data).is_valid())
