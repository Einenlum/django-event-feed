import pytest
from django.core import mail
from core.tests.helpers import create_event, create_user


@pytest.mark.django_db
def test_an_email_is_sent_when_another_attendee_than_the_author_joins_the_event():
    roger = create_user("roger", email="roger@roger.com")
    event = create_event(roger.profile)
    pierre = create_user("pierre")
    event.attendees.add(pierre.profile)
    event.save()

    assert len(mail.outbox) == 1
    message = mail.outbox[0]
    assert message.to == ["roger@roger.com"]


@pytest.mark.django_db
def test_no_email_is_sent_when_the_author_joins_their_event():
    roger = create_user("roger", email="roger@roger.com")
    event = create_event(roger.profile)
    event.attendees.remove(roger.profile)
    event.save()

    event.attendees.add(roger.profile)
    event.save()

    assert len(mail.outbox) == 0
