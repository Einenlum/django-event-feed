import pytest
from django.utils import timezone
from core.models import Event
from core.tests.helpers import create_country, create_city, create_user


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
