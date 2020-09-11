import pytest
from django.utils import timezone
from pprint import pprint
from api.models import Event
from api.tests.helpers import create_city, create_user, create_country, create_event


def authenticate_as(client, username, password):
    token = client.post(
        "/auth/authenticate/", {"username": username, "password": password}
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
def test_an_authenticated_user_can_create_an_event(api_client):
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
def test_an_anonymous_user_cannot_create_an_event(api_client):
    response = api_client.post(
        "/events/",
        {
            "title": "Some title",
            "description": "Some description",
            "location": "Some location",
            "city": 1,
            "start_date": timezone.now(),
            "end_date": timezone.now(),
        },
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_an_authenticated_user_can_see_the_detail_of_an_event(api_client):
    event = create_event()
    pierre = create_user("pierre", "password")
    authenticate_as(api_client, "pierre", "password")

    response = api_client.get(f"/events/{event.pk}/")
    assert response.status_code == 200
    assert response.data["title"] == event.title


@pytest.mark.django_db
def test_an_anonymous_user_cannot_see_the_detail_of_an_event(api_client):
    event = create_event()

    response = api_client.get(f"/events/{event.pk}/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_only_the_author_of_an_event_can_edit_a_piece_of_information(api_client):
    some_user = create_user("john", "password")
    event = create_event(some_user.profile)
    authenticate_as(api_client, "john", "password")

    response = api_client.patch(f"/events/{event.pk}/", {"title": "A new shiny title"})
    assert response.status_code == 200
    assert response.data["title"] == "A new shiny title"

    some_other_user = create_user("rico", "password")
    authenticate_as(api_client, "rico", "password")
    response = api_client.patch(f"/events/{event.pk}/", {"title": "You, dirty hacker"})
    assert response.status_code == 403


@pytest.mark.django_db
def test_only_the_author_of_an_event_can_replace_their_whole_event(api_client):
    pierre = create_user("pierre", "password")
    event = create_event(pierre.profile)
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

    raoul = create_user("raoul", "password")
    authenticate_as(api_client, "raoul", "password")
    response = api_client.put(
        f"/events/{event.pk}/",
        {
            "location": "Boxi",
            "title": "Hacked!",
            "author": pierre.profile.pk,
            "start_date": timezone.now(),
            "end_date": timezone.now(),
            "city": berlin.pk,
            "description": "A new shiny description",
        },
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_only_the_author_of_an_event_can_delete_it(api_client):
    pierre = create_user("pierre", "password")
    event = create_event(pierre.profile)
    authenticate_as(api_client, "pierre", "password")

    response = api_client.delete(f"/events/{event.pk}/")
    assert response.status_code == 204
    response = api_client.get("/events/")
    assert response.data == []

    event = create_event(pierre.profile)
    raoul = create_user("raoul", "password")
    authenticate_as(api_client, "raoul", "password")

    response = api_client.delete(f"/events/{event.pk}/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_a_user_can_attend_an_event(api_client):
    pierre = create_user("pierre", "password")
    event = create_event(pierre.profile)
    michel = create_user("michel", "password")
    authenticate_as(api_client, "michel", "password")

    event_detail_response = api_client.get(f"/events/{event.pk}/")
    assert len(event_detail_response.data["attendees"]) == 1

    join_response = api_client.post(f"/events/{event.pk}/attend/")
    assert join_response.status_code == 302

    event_detail_response = api_client.get(f"/events/{event.pk}/")
    assert len(event_detail_response.data["attendees"]) == 2


@pytest.mark.django_db
def test_someone_cannot_attend_an_event_twice(api_client):
    pierre = create_user("pierre", "password")
    event = create_event(pierre.profile)
    authenticate_as(api_client, "pierre", "password")

    response = api_client.post(f"/events/{event.pk}/attend/")
    assert response.status_code == 400


@pytest.mark.django_db
def test_one_can_removes_themselves_from_an_event(api_client):
    pierre = create_user("pierre", "password")
    event = create_event(pierre.profile)
    raoul = create_user("raoul", "password")
    event.attendees.add(raoul.profile)
    event.save()
    authenticate_as(api_client, "raoul", "password")

    event_detail_response = api_client.get(f"/events/{event.pk}/")
    assert len(event_detail_response.data["attendees"]) == 2

    response = api_client.delete(f"/events/{event.pk}/attend/")
    assert response.status_code == 302

    event_detail_response = api_client.get(f"/events/{event.pk}/")
    assert len(event_detail_response.data["attendees"]) == 1
