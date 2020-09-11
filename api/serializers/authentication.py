from rest_framework import serializers
from django.contrib.auth.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.HyperlinkedIdentityField(
        view_name="profiles_resource", read_only=True
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "profile",
        )
