from django.urls import path
from .views import EventCollectionAPIView, EventResourceAPIView

urlpatterns = [
    path(
        r"events/",
        EventCollectionAPIView.as_view(),
        name="events_collection",
    ),
    path(r"events/<pk>/", EventResourceAPIView.as_view(), name="events_resource"),
]
