from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework import views, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from users.models import UserAccount
from api.v1.auth.serializers import TokenSerializer
from .serializers import UserSerializer


class CreateUserView(views.APIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_serializer(self, **kwargs):
        return self.serializer_class(**kwargs)
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = Token.objects.create(user=user)
            token_serializer = TokenSerializer(instance=token)
            return Response({"user": serializer.data, "token": token_serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):

    def retrieve(self, request, pk=None):
        serializer = UserSerializer(instance=request.user, read_only=True)
        return Response(serializer.data, status=status.HTTP_200_OK)