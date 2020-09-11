from django.contrib.auth.models import User
from drf_yasg.utils import get_serializer_class
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken as BaseObtainAuthToken
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from ..serializers.authentication import CreateUserSerializer, UserSerializer


class RegisterUser(CreateAPIView):
    model = User
    serializer_class = CreateUserSerializer

    def to_representation(self, instance):
        serializer = UserSerializer(instance)

        return serializer.data


class ObtainAuthToken(BaseObtainAuthToken):
    # Here we override the method where the token is generated
    # to generate a new token everytime
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        try:
            token = Token.objects.get(user=user)
            token.delete()
        except Token.DoesNotExist:
            pass
        token = Token.objects.create(user=user)

        return Response({"token": token.key})
