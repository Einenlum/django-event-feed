from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import EventCollectionAPIView, EventResourceAPIView


urlpatterns = [
    path("auth/authenticate/", obtain_auth_token),
    path(
        r"events/",
        EventCollectionAPIView.as_view(),
        name="events_collection",
    ),
    path(r"events/<pk>/", EventResourceAPIView.as_view(), name="events_resource"),
]
