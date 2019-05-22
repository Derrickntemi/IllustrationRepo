from django.urls import reverse
from rest_framework.views import status
from .models import Articles
from .serializers import ArticlesSerializer
import json
from rest_framework.test import APITestCase, APIClient
from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

# testing model Article


class ArticlesModelTest(APITestCase):
    def setUp(self):
        self.article = Articles.objects.create(
            title="The Gang of four",
            author="Derrick kimathi"
        )

    def test_articles(self):
        # ensures method created in setup method exists
        self.assertEqual(self.article.title, "The Gang of four")
        self.assertEqual(self.article.author, "Derrick kimathi")
        self.assertEqual(str(self.article),
                         "The Gang of four : Derrick kimathi")


# test the views
class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_article(title="", author=""):
        # create an article in the database with parameters author and title
        if title != None and author != None:
            Articles.objects.create(title=title, author=author)

    def make_request(self, kind="post", **kwargs):

        # Make a post request to create an article
        if kind == "post":
            return self.client.post(
                reverse(
                    "create-article",
                    kwargs={
                        "version": kwargs["version"]
                    }
                ),
                data=json.dumps(kwargs["data"]),
                content_type='application/json'
            )
        elif kind == "put":
            return self.client.put(
                reverse(
                    "article-info",
                    kwargs={
                        "version": kwargs["version"],
                        "pk": kwargs["id"]
                    }
                ),
                data=json.dumps(kwargs["data"]),
                content_type='application/json'
            )
        else:
            return None

    # fetch an article for db using id
    def fetch_article(self, pk=0):
        return self.client.get(
            reverse(
                "article-info",
                kwargs={
                    "version": "v1",
                    "pk": pk
                }
            )
        )
    # delete an article from db using id

    def delete_article(self, pk=0):
        return self.client.delete(
            reverse(
                "article-info",
                kwargs={
                    "version": "v1",
                    "pk": pk
                }
            )
        )
    # user login with parameters username and password

    def login_user(self, username="", password=""):
        url = reverse(
            "auth-login",
            kwargs={
                "version": "v1"
            }
        )
        return self.client.post(
            url,
            data=json.dumps({
                "username": username,
                "password": password
            }),
            content_type="application/json"
        )

    def login_client(self, username="", password=""):
        # get a token from DRF(tokenbased authentication)
        response = self.client.post(
            reverse("create-token"),
            data=json.dumps(
                {
                    'username': username,
                    'password': password
                }
            ),
            content_type='application/json'
        )
        self.token = response.data['token']
        # set the token in the header(Authorization header)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.client.login(username=username, password=password)
        return self.token

    def register_user(self, username="", password="", email=""):
        return self.client.post(
            reverse(
                "auth-register",
                kwargs={
                    "version": "v1"
                }
            ),
            data=json.dumps(
                {
                    "username": username,
                    "password": password,
                    "email": email
                }
            ),
            content_type='application/json'
        )

    def setUp(self):
        # create an admin user
        self.user = User.objects.create_superuser(
            username="dntemi",
            email="derrickntemi@gmail.com",
            password="derrick123",
            first_name="derrick",
            last_name="ntemi",
        )
        # add testing data
        self.create_article("the programming mastery", "austin mwenda")
        self.create_article("automata", "professor derrick ntemi")
        self.create_article("learning data science", "Derrick ntemi")
        self.create_article(
            "under the machine learning umbrella", "Maureen ntemi")
        self.create_article("machine learning", "Brandon mawira")
        self.create_article("unsupervised learning", "Derrick kimathi")

        self.invalid_data = {
            "title": "",
            "author": ""
        }

        self.valid_data = {
            "title": "test article",
            "author": "test author"
        }

        self.valid_article_id = 1
        self.invalid_article_id = 20


class GetAllArticlesTest(BaseViewTest):

    def test_get_all_articles(self):

        # testing retrieval of all articles created in setup method
        self.login_client('dntemi', 'derrick123')
        # hit the API endpoint
        response = self.client.get(
            reverse("create-article", kwargs={"version": "v1"})
        )
        # retrieve the data from database
        anticipated_res = Articles.objects.all()
        serialized_res = ArticlesSerializer(anticipated_res, many=True)
        self.assertEqual(response.data, serialized_res.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SingleArticleTest(BaseViewTest):

    def test_get_article(self):
        # testing retrieval of single article using id
        self.login_client('dntemi', 'derrick123')
        # hit the API endpoint
        response = self.fetch_article(self.valid_article_id)
        # fetch the data from database
        article = get_object_or_404(Articles, pk=self.valid_article_id)
        serialized_res = ArticlesSerializer(article)
        self.assertEqual(response.data, serialized_res.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # check for an article that does not exist
        response = self.fetch_article(self.invalid_article_id)
        self.assertEqual(
            response.data["message"],
            "Article  id: 50 doesn't exist"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AddArticleTest(BaseViewTest):

    def test_create_article(self):
        # testing creation of a single article
        self.login_client('dntemi', 'derrick123')
        # hit the API endpoint
        response = self.make_request(
            kind="post",
            version="v1",
            data=self.valid_data
        )

        print(response)
        self.assertEqual(response.data, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # testing with invalid data
        response = self.make_request(
            kind="post",
            version="v1",
            data=self.invalid_data
        )
        self.assertEqual(
            response.data["message"],
            "title and author are required to add an article"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateArticleTest(BaseViewTest):

    def test_update_an_article(self):

        # testing update of data in db of article 5 with correct data and article 4 with wrong data
        self.login_client('dntemi', 'derrick123')
        # hit the API endpoint
        response = self.make_request(
            kind="put",
            version="v1",
            id=3,
            data=self.valid_data
        )
        self.assertEqual(response.data, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test with invalid data article id 4
        response = self.make_request(
            kind="put",
            version="v1",
            id=4,
            data=self.invalid_data
        )
        self.assertEqual(
            response.data["message"],
            "title and author  required to add an article"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteArticleTest(BaseViewTest):

    def test_delete_an_article(self):
        # testing deleting an article with the ID
        self.login_client('dntemi', 'derrick123')
        # hit the API endpoint
        response = self.delete_article(1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # test with invalid data
        response = self.delete_article(20)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class LoginUserTest(BaseViewTest):

    # testing authentication endpoint
    def test_login_user_with_valid_credentials(self):
        # test login with valid credentials
        response = self.login_user("dntemi", "derrick123")
        # assert token key exists
        self.assertIn("token", response.data)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test login with invalid credentials
        response = self.login_user("mathwiti", "makeki")
        # assert status code is 401 (UNAUTHORIZED)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RegisterUserTest(BaseViewTest):

    # user registration test
    def test_register_a_user(self):
        response = self.register_user(
            "test_user", "pass_test", "test_user@gmail.com")
        # assert status code is 201 CREATED
        self.assertEqual(response.data["username"], "test_user")
        self.assertEqual(response.data["email"], "test_user@gmail.com")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # test with invalid data
        response = self.register_user()
        # assert status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
