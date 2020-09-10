from rest_framework.authentication import TokenAuthentication
from django.utils import timezone
from eventfeed import settings
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class BearerTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"

    # We override this method to be able to limit the validity of the token
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related("user").get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_("Invalid token."))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_("User inactive or deleted."))

        age_of_the_token_in_minutes = (
            timezone.now() - token.created
        ).total_seconds() / 60

        if (
            age_of_the_token_in_minutes
            > settings.MINUTES_OF_VALIDITY_FOR_A_BEARER_TOKEN
        ):
            raise exceptions.AuthenticationFailed(_("Token has expired."))

        return (token.user, token)
