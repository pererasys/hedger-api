from users.models import UserAccount
from .serializers import UserSerializer
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes


class CreateUserView(views.APIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_serializer(self, **kwargs):
        return self.serializer_class(**kwargs)
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
