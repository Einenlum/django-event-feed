from rest_framework import serializers
from .models import Event


class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "author",
            "title",
            "description",
            "start_date",
            "end_date",
            "location",
            "city",
            "canceled",
        )


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "id",
            "author",
            "title",
            "description",
            "start_date",
            "end_date",
            "attendees",
            "location",
            "city",
            "canceled",
        )
