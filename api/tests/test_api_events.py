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


@pytest.mark.django_db
def test_events_collection_api(api_client):
    roger = create_user("roger")
    france = create_country("France")
    paris = create_city(france, "Paris")

    # No events so far
    response = api_client.get("/events/")
    assert response.status_code == 200
    assert response.data == []

    # Event creation
    response = api_client.post(
        "/events/",
        {
            "title": "Some title",
            "description": "Some description",
            "location": "Some location",
            "city": paris.pk,
            "author": roger.pk,
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
    assert response.data[0]["attendees"] == [roger.pk]


@pytest.mark.django_db
def test_events_get_api(api_client):
    event = create_event()

    response = api_client.get(f"/events/{event.pk}/")
    assert response.status_code == 200
    assert response.data["title"] == event.title


@pytest.mark.django_db
def test_events_patch_api(api_client):
    event = create_event()

    response = api_client.patch(f"/events/{event.pk}/", {"title": "A new shiny title"})
    assert response.status_code == 200
    assert response.data["title"] == "A new shiny title"


@pytest.mark.django_db
def test_events_existing_put_api(api_client):
    event = create_event()
    pierre = create_user("pierre")
    germany = create_country("Germany")
    berlin = create_city(germany, "Berlin")

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
def test_events_not_existing_put_api(api_client):
    pierre = create_user("pierre")
    germany = create_country("Germany")
    berlin = create_city(germany, "Berlin")

    response = api_client.put(
        f"/events/78/",
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
    assert response.data["id"] == 78


@pytest.mark.django_db
def test_events_delete_api(api_client):
    event = create_event()
    response = api_client.delete(f"/events/{event.pk}/")
    assert response.status_code == 204
    response = api_client.get("/events/")
    assert response.data == []
