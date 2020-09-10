import pytest
from django.utils import timezone
from pprint import pprint
from api.models import Event
from api.tests.helpers import create_city, create_user, create_country


def create_event():
    roger = create_user("roger")
    france = create_country("France")
    paris = create_city(france, "Paris")
    event = Event.objects.create(
        author=roger.profile,
        city=paris,
        location="Under the Eiffer Tower",
        start_date=timezone.now(),
        end_date=timezone.now(),
        title="Some weird title",
        description="Some funny description",
    )

    return event


def authenticate_as(client, username, password):
    token = client.post(
        "/auth/authenticate/", {"username": "pierre", "password": "password"}
    ).data["token"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")


@pytest.mark.django_db
def test_events_collection_api(api_client):
    # No events so far
    response = api_client.get("/events/")
    assert response.status_code == 200
    assert response.data == []

    event = create_event()

    # Get all collection again
    response = api_client.get("/events/")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["title"] == event.title
    assert response.data[0]["attendees"] == [1]


@pytest.mark.django_db
def test_events_post_to_collection_api(api_client):
    pierre = create_user("pierre", "password")
    france = create_country("France")
    paris = create_city(france, "Paris")
    authenticate_as(api_client, "pierre", "password")

    # Event creation
    response = api_client.post(
        "/events/",
        {
            "title": "Some title",
            "description": "Some description",
            "location": "Some location",
            "city": paris.pk,
            "author": pierre.pk,
            "start_date": timezone.now(),
            "end_date": timezone.now(),
        },
    )
    assert response.status_code == 201

    # Get all collection again
    response = api_client.get("/events/")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["title"] == "Some title"
    assert response.data[0]["attendees"] == [pierre.pk]


@pytest.mark.django_db
def test_events_get_api(api_client):
    event = create_event()
    pierre = create_user("pierre", "password")
    authenticate_as(api_client, "pierre", "password")

    response = api_client.get(f"/events/{event.pk}/")
    assert response.status_code == 200
    assert response.data["title"] == event.title


@pytest.mark.django_db
def test_events_patch_api(api_client):
    event = create_event()
    pierre = create_user("pierre", "password")
    authenticate_as(api_client, "pierre", "password")

    response = api_client.patch(f"/events/{event.pk}/", {"title": "A new shiny title"})
    assert response.status_code == 200
    assert response.data["title"] == "A new shiny title"


@pytest.mark.django_db
def test_events_put_api(api_client):
    event = create_event()
    pierre = create_user("pierre", "password")
    germany = create_country("Germany")
    berlin = create_city(germany, "Berlin")
    authenticate_as(api_client, "pierre", "password")

    response = api_client.put(
        f"/events/{event.pk}/",
        {
            "location": "Boxi",
            "title": "A new shiny title",
            "author": pierre.profile.pk,
            "start_date": timezone.now(),
            "end_date": timezone.now(),
            "city": berlin.pk,
            "description": "A new shiny description",
        },
    )
    assert response.status_code == 200
    assert response.data["title"] == "A new shiny title"
    assert response.data["location"] == "Boxi"


@pytest.mark.django_db
def test_events_delete_api(api_client):
    event = create_event()
    pierre = create_user("pierre", "password")
    authenticate_as(api_client, "pierre", "password")

    response = api_client.delete(f"/events/{event.pk}/")
    assert response.status_code == 204
    response = api_client.get("/events/")
    assert response.data == []
