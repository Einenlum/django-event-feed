import pytest
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from api.tests.helpers import create_event
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
def test_a_new_token_is_always_generated_after_authentication(api_client):
    User.objects.create_user("paul", password="password")

    token_1 = api_client.post(
        "/auth/authenticate/", {"username": "paul", "password": "password"}
    ).data["token"]
    token_2 = api_client.post(
        "/auth/authenticate/", {"username": "paul", "password": "password"}
    ).data["token"]

    assert token_1 != token_2


@pytest.mark.django_db
def test_token_is_valid_only_for_twenty_four_hours(api_client):
    paul = User.objects.create_user("paul", password="password")
    event = create_event()

    # it's 18 hours old, so still valid
    token_18h_old = Token.objects.create(user=paul)
    # We use this weird trick with a queryset to be able to update the created field
    # although it's non editable because of auto_now_add…
    # Took me a few hours to understand the problem.
    # See https://stackoverflow.com/a/11316645/3524372
    Token.objects.filter(pk=token_18h_old.pk).update(
        created=(timezone.now() - timedelta(seconds=60 * 60 * 18))
    )
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_18h_old.key}")
    response = api_client.get(f"/events/{event.pk}/")
    assert response.status_code == 200

    # Now it's 25 hours old
    token_25h_old = token_18h_old
    # Same weird trick as above
    Token.objects.filter(pk=token_25h_old.pk).update(
        created=(timezone.now() - timedelta(60))
    )
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_25h_old.key}")
    response = api_client.get(f"/events/{event.pk}/")
    # The token is not valid anymore
    assert response.status_code == 401
