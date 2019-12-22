from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Songs
from .serializers import SongsSerializer

class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_song(title="", artist="" ):
        if title != "" and artist != "":
            Songs.objects.create(title=title, artist=artist)

    def setup(self):
        #test data

        self.create_song("teri sanam","arjit")
        self.create_song("dhadkan", "sabar")
        self.create_song("made in india","lucky ali")

class GetAllSongsTest(BaseViewTest):

    def test_get_all_songs(self):
        """
        to ensure all songs are added in setUp method exist when
        we make a Get request method to songs/endpoint
        """

        #hit the API endpoint

        response = self.client.get(
            reverse("songs-all", kwargs = {"version": "v1"})
        )

        #fetch data from database
        expected = Songs.objects.all()
        serialized = SongsSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
