from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken as BaseObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
)
from django.http import HttpResponse
from .models import Event
from .serializers import EventSerializer, CreateEventSerializer
from .custom_permissions import EventObjectPermission


class EventCollectionAPIView(ListCreateAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateEventSerializer

        return super().get_serializer_class()


class EventResourceAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated, EventObjectPermission]


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
