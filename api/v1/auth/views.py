'''
Written by Andrew Perera
Copyright 2020
'''

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from api.v1.users.serializers import UserSerializer
from .serializers import LoginSerializer, TokenSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def get_serializer(self, **kwargs):
        return self.serializer_class(**kwargs)

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})

        # Throw errors if login failed
        serializer.is_valid(raise_exception=True)

        token, created = Token.objects.get_or_create(user=serializer.validated_data)
        token_serializer = TokenSerializer(instance=token)
        user_serializer = UserSerializer(instance=serializer.validated_data)

        return Response({"token": token_serializer.data, "user": user_serializer.data}, status=status.HTTP_200_OK)


class LogoutView(APIView):

    def post(self, request):
        request.auth.delete()
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
