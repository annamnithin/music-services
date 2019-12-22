from django.shortcuts import render

# Create your views here.

from rest_framework import generics , status
from rest_framework.response import Response

from .models import Songs
from .serializers import SongsSerializer, TokenSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# GET THE JWT settings, add these lines after the import/ from lines
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """

    # this permission class override the global permission
    # class setting

    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self,request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            # login saves the user's ID in the session
            # using Django session framework
            login(request, user)
            serializer = TokenSerializer(data = {
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status = status.HTTP_401_UNAUTHORIZED)


class ListSongsView(generics.ListAPIView):
    """
    Provides a get method handler
    """
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer
    permission_classes = (permissions.IsAuthenticated,)




