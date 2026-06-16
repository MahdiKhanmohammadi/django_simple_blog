from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from blog.models import Category, Post
from blog.api.serializer import CategoryModelSerializer, PostListModelSerializer, PostWriteModelSerializer
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


class CategoryViewSetTest(APITestCase):

    def setUp(self):
        self.path = '/blog/api/category/'
        category_count = 15
        for cat_id in range(category_count):
            Category.objects.create(
                title=f"api_category_title: {cat_id}")

        self.UserModel = get_user_model()
        self.test_user = self.UserModel(
            email="test_email@gmail.com", is_active=True)
        self.test_user.set_password('1234')
        self.test_user.save()

        self.test_user_token = Token.objects.create(user=self.test_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.test_user_token.key)

    # region REQUEST_METHOD: GET

    def test_category_list_valid_url(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_single_category_valid_url(self):
        path = self.path + "1/"
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_single_category_get_valid_data(self):
        # "1/ is category id for get and find specific category object"
        path = self.path + "1/"
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTP_200_OK)
        get_category = Category.objects.get(pk=1)
        self.assertEqual(
            response.data, CategoryModelSerializer(get_category).data)

    def test_pagination_category_list(self):
        response = self.client.get(self.path)
        self.assertIn('next', response.data)
        self.assertEqual("page=2",
                         response.data.get("next").split('?')[1])

        # check valid data count show in page 2
        response_page_2 = self.client.get(self.path+"?page=2")
        self.assertEqual(5, len(response_page_2.data.get('results')))

    # endregion

    # REQUEST_METHOD: POST

    def test_post_category(self):
        data = {
            "title": "new test category",
            "status": True
        }

        response = self.client.post(self.path, data, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertTrue(Category.objects.get(title="new test category"))

    # REQUEST_METHOD: PUT
    def test_put_category(self):
        # "1/ is category id for get and find specific category object"
        path = self.path + '1/'
        data = {
            'title': 'api_category_title: 0',
            'status': True
        }
        response = self.client.put(path, data, format='json')

        self.assertEqual(response.status_code, 200)

        get_category = Category.objects.get(pk=1)

        self.assertEqual(
            response.data, CategoryModelSerializer(get_category).data)

    # REQUEST_METHOD: PATCH

    def test_patch_category(self):
        # "1/ is category id for get and find specific category object"
        path = self.path + '1/'
        data = {
            'status': True
        }
        response = self.client.patch(path, data, format='json')
        self.assertEqual(response.status_code, 200)
        get_category = Category.objects.get(pk=1)
        self.assertEqual(
            response.data, CategoryModelSerializer(get_category).data)

    def test_delete_category(self):
        # "1/ is category id for get and find specific category object"
        path = self.path + '1/'
        response = self.client.delete(path)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(pk=1).exists())


class PostViewSetTest(APITestCase):

    def setUp(self):
        self.path = '/blog/api/post/'

        self.UserModel = get_user_model()
        self.user = self.UserModel.objects.create(
            email="email@email.com", password='1234')

        self.UserModel = get_user_model()
        self.test_user = self.UserModel(
            email="test_email@gmail.com", is_active=True)
        self.test_user.set_password('1234')
        self.test_user.save()

        self.test_user_token = Token.objects.create(user=self.test_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.test_user_token.key)

        post_count = 15
        self.category = Category.objects.create(title='cat_title')
        for post_id in range(post_count):
            Post.objects.create(
                title=f"api_post_title: {post_id}",
                content=f"content- {post_id}",
                author=self.user,
                category=self.category

            )

        # crete test post object for test method post and put
        self.test_object_for_put_or_post_method = {
            "title": "new test post",
            "status": True,
            'author': self.user.pk,
            'category': self.category.pk,
            'content': "new content for new object"
        }
    # region REQUEST_METHOD: GET

    def test_post_list_valid_url(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_single_post_valid_url(self):
        path = self.path + "1/"
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_single_post_get_valid_data(self):
        # "1/ is post id for get and find specific category object"
        path = self.path + "1/"
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTP_200_OK)
        get_post = Post.objects.get(pk=1)
        self.assertEqual(
            response.data, PostListModelSerializer(get_post).data)

    def test_pagination_post_list(self):
        response = self.client.get(self.path)
        self.assertIn('next', response.data)
        self.assertEqual("page=2",
                         response.data.get("next").split('?')[1])

        # check valid data count show in page 2
        response_page_2 = self.client.get(self.path+"?page=2")
        self.assertEqual(5, len(response_page_2.data.get('results')))

    # endregion

    # REQUEST_METHOD: POST

    def test_post_method_post(self):

        response = self.client.post(
            self.path, self.test_object_for_put_or_post_method, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertTrue(Post.objects.get(title="new test post"))

    # REQUEST_METHOD: PUT
    def test_put_post(self):
        # "1/ is post id for get and find specific post object"
        path = self.path + '1/'

        response = self.client.put(
            path, self.test_object_for_put_or_post_method, format='json')

        self.assertEqual(response.status_code, 200)

        get_post = Post.objects.get(pk=1)

        self.assertEqual(
            response.data, PostWriteModelSerializer(get_post).data)

    # REQUEST_METHOD: PATCH

    def test_patch_post(self):
        # "1/ is post id for get and find specific post object"
        path = self.path + '1/'
        data = {
            'status': True
        }
        response = self.client.patch(path, data, format='json')
        self.assertEqual(response.status_code, 200)
        get_post = Post.objects.get(pk=1)
        self.assertEqual(
            response.data, PostWriteModelSerializer(get_post).data)

    def test_delete_post(self):
        # "1/ is post id for get and find specific post object"
        path = self.path + '1/'
        response = self.client.delete(path)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(pk=1).exists())
