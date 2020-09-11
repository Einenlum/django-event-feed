import pytest
from api.tests.helpers import create_user, create_event, authenticate_as


@pytest.mark.django_db
def test_an_event_detail_leads_to_attendees_url(api_client):
    event = create_event()
    attendee = create_user("attendee", "password")
    event.attendees.add(attendee.profile)
    event.save()
    authenticate_as(api_client, "attendee", "password")

    response = api_client.get(f"/events/{event.pk}/")
    attendees_urls = response.data["attendees"]
    response = api_client.get(attendees_urls[0])
    assert response.status_code == 200


@pytest.mark.django_db
def test_anonymous_users_cannot_access_profile_details(api_client):
    user = create_user("john")
    response = api_client.get(f"/profiles/{user.profile.pk}/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_authenticated_users_can_access_profile_details(api_client):
    john = create_user("john")
    jim = create_user("jim", "password")
    authenticate_as(api_client, "jim", "password")
    response = api_client.get(f"/profiles/{jim.profile.pk}/")

    assert response.status_code == 200
    assert response.data["id"] == jim.profile.id
    assert response.data["username"] == jim.username
