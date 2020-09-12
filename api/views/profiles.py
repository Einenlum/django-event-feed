from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from core.models import Profile
from ..serializers.profiles import ProfileSerializer


class ProfileView(RetrieveAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
