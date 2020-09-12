import pytest
import os
import time
from core.tests.helpers import create_event, create_user, WithEmails, try_until_seconds


def count_files(path):
    return len(os.listdir(path))


@pytest.mark.django_db
def test_an_email_is_sent_when_another_attendee_than_the_author_joins_the_event():
    """
    This test is flaky. Only green when this module is launch alone.
    Still trying to figure out why.
    """
    with WithEmails() as email_path:
        roger = create_user("roger", email="roger@roger.com")
        event = create_event(roger.profile)
        pierre = create_user("pierre")
        event.attendees.add(pierre.profile)
        event.save()

        # Seems like there is a delay, even if we use CELERY EAGER ¯\_(ツ)_/¯
        assert try_until_seconds(5, lambda: count_files(email_path) == 1)


@pytest.mark.django_db
def test_no_email_is_sent_when_the_author_joins_their_event():
    with WithEmails() as email_path:
        roger = create_user("roger", email="roger@roger.com")
        event = create_event(roger.profile)
        event.attendees.remove(roger.profile)
        event.save()

        event.attendees.add(roger.profile)
        event.save()

        time.sleep(1)
        assert count_files(email_path) == 0
