'''
Written by Andrew Perera
Copyright 2020
'''

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer, TokenSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def get_serializer(self, **kwargs):
        return self.serializer_class(**kwargs)

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data

        token, created = Token.objects.get_or_create(user=user)

        token_serializer = TokenSerializer(instance=token)
        return Response(token_serializer.data, status=status.HTTP_200_OK)
