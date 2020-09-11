from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from ..models import Event
from ..serializers.events import (
    EventSerializer,
    CreateEventSerializer,
    EditEventSerializer,
    CollectionEventSerializer,
)
from ..custom_permissions import EventObjectPermission


class EventCollectionAPIView(ListCreateAPIView):
    serializer_class = CollectionEventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateEventSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.profile)


class EventResourceAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated, EventObjectPermission]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return EditEventSerializer

        return super().get_serializer_class()


@api_view(["POST", "DELETE"])
def attend_an_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == "POST":
        if request.user.profile in event.attendees.all():
            raise ValidationError("You are already attending this event")

        event.attendees.add(request.user.profile)
        event.save()

        return redirect(event.get_absolute_url())

    # DELETE
    if request.user.profile in event.attendees.all():
        event.attendees.remove(request.user.profile)
        event.save()

    return redirect(event.get_absolute_url())
