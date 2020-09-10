from django.contrib import admin
from .models import Country, City, Profile, Event

admin.site.register(Country)
admin.site.register(City)
admin.site.register(Profile)
admin.site.register(Event)
