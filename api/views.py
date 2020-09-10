from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
)
from django.http import HttpResponse
from .models import Event
from .serializers import EventSerializer, CreateEventSerializer


class EventCollectionAPIView(ListCreateAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateEventSerializer

        return super().get_serializer_class()


class EventResourceAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
