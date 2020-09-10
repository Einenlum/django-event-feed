import pytest
from django.utils import timezone
from django.contrib.auth.models import User
from api.models import Country, City, Event


def create_user(username):
    return User.objects.create_user(username)


def create_country(name):
    return Country.objects.create(name=name)


def create_city(country, name):
    return City.objects.create(country=country, name=name)


@pytest.mark.django_db
def test_an_event_has_its_author_as_attendee_by_default():
    user = create_user("john")
    france = create_country("France")
    paris = create_city(france, "Paris")

    event = Event.objects.create(
        author=user.profile,
        title="title",
        description="description",
        start_date=timezone.now(),
        end_date=timezone.now(),
        city=paris,
        location="Under the Eiffel Tower",
    )
    assert user.profile in event.attendees.all()
    assert event.attendees.count() == 1
