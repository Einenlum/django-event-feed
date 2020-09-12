import os
import pathlib
import shutil
import time
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import Country, City, Event, Profile
from django.conf import settings


def create_user(username, password=None, email=None):
    return User.objects.create_user(username, email=email, password=password)


def create_country(name: str):
    return Country.objects.create(name=name)


def create_city(country: Country, name: str):
    return City.objects.create(country=country, name=name)


def create_event(profile=None):
    if not profile:
        profile = create_user("roger", "password").profile
    france = create_country("France")
    paris = create_city(france, "Paris")
    event = Event.objects.create(
        author=profile,
        city=paris,
        location="Under the Eiffer Tower",
        start_date=timezone.now(),
        end_date=timezone.now(),
        title="Some weird title",
        description="Some funny description",
    )

    return event


class WithEmails(object):
    def __enter__(self):
        if os.path.exists(settings.EMAIL_FILE_PATH):
            shutil.rmtree(settings.EMAIL_FILE_PATH)
        # we create the full dir if it does not exist
        pathlib.Path(settings.EMAIL_FILE_PATH).mkdir(parents=True, exist_ok=True)

        return settings.EMAIL_FILE_PATH

    def __exit__(self, *args):
        if os.path.exists(settings.EMAIL_FILE_PATH):
            shutil.rmtree(settings.EMAIL_FILE_PATH)


def try_until_seconds(seconds, func):
    start = time.time()
    max_end = time.time() + seconds

    while time.time() < max_end:
        if func():
            return True

    return False
