from django.urls import path
from .views.events import EventCollectionAPIView, EventResourceAPIView
from .views.authentication import ObtainAuthToken


urlpatterns = [
    path("auth/authenticate/", ObtainAuthToken.as_view()),
    path(
        r"events/",
        EventCollectionAPIView.as_view(),
        name="events_collection",
    ),
    path(r"events/<pk>/", EventResourceAPIView.as_view(), name="events_resource"),
]
