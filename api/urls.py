from django.urls import path
from .views import event_collection, event_element

urlpatterns = [
    path(r"events/", event_collection),
    path(r"events/<pk>/", event_element),
]
