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

    def setup(self):

        # creating admin user

        self.user = User.objects.create_superuser(
            username = "test_user",
            email = "test@gmail.com",
            password = "testing",
            first_name = "test",
            last_name = "user",
        )
        
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



class GetAllSongsTest(BaseViewTest):

    def test_get_all_songs(self):
        """
        to ensure all songs are added in setUp method exist when
        we make a Get request method to songs/endpoint
        """

        # hit the API endpoint

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


