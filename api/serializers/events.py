from rest_framework import serializers
from ..models import Event


class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "title",
            "description",
            "start_date",
            "end_date",
            "location",
            "city",
            "canceled",
        )


class EditEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "title",
            "description",
            "start_date",
            "end_date",
            "location",
            "city",
            "canceled",
        )


class CollectionEventSerializer(serializers.ModelSerializer):
    author = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="profiles_resource"
    )

    class Meta:
        model = Event
        fields = (
            "id",
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
    attendees = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="profiles_resource"
    )
    author = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="profiles_resource"
    )

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
