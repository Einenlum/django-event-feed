from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from .views.events import EventCollectionAPIView, EventResourceAPIView, attend_an_event
from .views.authentication import ObtainAuthToken
from .views.profiles import ProfileView

schema_view = get_schema_view(
    openapi.Info(
        title="Event Feed API",
        default_version="v1",
        description="Some toy project API to play with DRF",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("doc/", schema_view.with_ui("swagger", cache_timeout=0)),
    path("auth/authenticate/", ObtainAuthToken.as_view()),
    path(
        r"events/",
        EventCollectionAPIView.as_view(),
        name="events_collection",
    ),
    path(r"events/<pk>/attend/", attend_an_event, name="events_attend"),
    path(r"events/<pk>/", EventResourceAPIView.as_view(), name="events_resource"),
    path(r"profiles/<pk>/", ProfileView.as_view(), name="profiles_resource"),
]
