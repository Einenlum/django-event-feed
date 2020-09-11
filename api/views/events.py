from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from ..models import Event
from ..serializers import EventSerializer, CreateEventSerializer, EditEventSerializer
from ..custom_permissions import EventObjectPermission


class EventCollectionAPIView(ListCreateAPIView):
    serializer_class = EventSerializer
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
