from rest_framework import serializers
from core.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    created_events = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="events_resource"
    )
    attending_events = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="events_resource"
    )

    class Meta:
        model = Profile
        fields = (
            "id",
            "username",
            "created_events",
            "attending_events",
        )

    def get_username(self, obj):
        return obj.user.username
