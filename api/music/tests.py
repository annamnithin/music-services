import json

from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Songs
from .serializers import SongsSerializer
from django.contrib.auth.models import User


class BaseViewTest(APITestCase):
    client = APIClient()

    def setUp(self):

        # creating admin user

        self.user = User.objects.create_superuser (
            username = "test_user" ,
            email = "test@mail.com" ,
            password = "testing" ,
            first_name = "test" ,
            last_name = "user" ,
        )
        # self.user.save()
        # test data

        self.create_song("teri sanam","arjit")
        self.create_song("dhadkan", "sabar")
        self.create_song("made in india","lucky ali")

    @staticmethod
    def create_song(title="", artist=""):
        if title != "" and artist != "":
            Songs.objects.create(title=title, artist=artist)

    def login_a_user(self, username="", password=""):

        url = reverse(
            "auth-login",
            kwargs = {
                "version": "v1"
            })
        return self.client.post(
            url,
            data = json.dumps({
                    "username": username,
                    "password": password
                }),
            content_type = "application/json"
        )

    def login_client(self, username="", password=""):
        # get a token from DRF
        response = self.client.post(
            reverse('create-token'),
            data = json.dumps(
                {
                    'username': username,
                    'password': password
                }
            ),
            content_type = "application/json"
        )
        print(response.data['token'])
        self.token = response.data['token']
        #set the token in header
        self.client.credentials(
            HTTP_AUTHORIZATION ='Bearer ' + self.token
        )
        self.client.login(username=username, password=password)
        return self.token



class GetAllSongsTest(BaseViewTest):

    def test_get_all_songs(self):
        """
        to ensure all songs are added in setUp method exist when
        we make a Get request method to songs/endpoint
        """

        # hit the API endpoint
        self.login_client('test_user', 'testing')
        response = self.client.get(
            reverse("songs-all", kwargs = {"version": "v1"})
        )

        # fetch data from database
        expected = Songs.objects.all()
        serialized = SongsSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthLoginUserTest(BaseViewTest):

    """
    Test for auth/login/ endpoint
    """

    def test_login_user_with_valid_credentials(self):
        # test login with valid credentials
        # users = User.objects.get(username="test_user")
        songs = Songs.objects.all()
        print("songs=",songs)
        # print(users)
        response = self.login_a_user("test_user", "testing")
        print(response)
        # assert token key exists
        self.assertIn("token", response.data)

        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test login with invalid credentials
        response = self.login_a_user("anonymus", "124")

        # assert status is 401 UNAUTHOROZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthRegisterUserTest(BaseViewTest):
    """
    Test for auth/register/end point
    """
    def test_register_a_user_with_valid_data(self):
        url = reverse(
            "auth-register",
            kwargs = {
                "version": "v1"
            }
        )
        response = self.client.post(
            url,
            data = json.dumps(
                {
                    "username": "new_user",
                    "password": "new_pass",
                    "email": "new_user@gmail.com"
                }
            ),
            content_type = "application/json"
        )
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_register_a_user_with_invalid_data(self):
        url = reverse(
            "auth-register",
            kwargs = {
                "version": "v1"
            }
        )
        response = self.client.post(
            url,
            data = json.dumps(
                {
                    "username": "",
                    "password": "",
                    "email": ""

                }
            ),
            content_type = "application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
