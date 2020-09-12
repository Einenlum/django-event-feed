from django.contrib.auth.models import User
from django.utils import timezone
from core.models import Country, City, Event


def create_user(username, password=None):
    return User.objects.create_user(username, password=password)


def create_country(name):
    return Country.objects.create(name=name)


def create_city(country, name):
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
