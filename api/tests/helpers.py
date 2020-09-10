from django.contrib.auth.models import User
from api.models import Country, City, Event


def create_user(username):
    return User.objects.create_user(username)


def create_country(name):
    return Country.objects.create(name=name)


def create_city(country, name):
    return City.objects.create(country=country, name=name)
