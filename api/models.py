from django.db import models
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, models.CASCADE, related_name="profile")

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User, dispatch_uid="create_profile_on_user_creation")
def create_profile_on_user_creation(sender, **kwargs):
    user = kwargs.get("instance")
    profile = Profile(user=user)
    profile.save()


class Country(models.Model):
    name = models.CharField(max_length=255, blank=False)

    class Meta:
        verbose_name_plural = "countries"

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255, blank=False)
    country = models.ForeignKey(Country, models.CASCADE, blank=False)

    class Meta:
        verbose_name_plural = "cities"

    def __str__(self):
        return f"{self.name} ({self.country})"


class Event(models.Model):
    author = models.ForeignKey(Profile, models.CASCADE, related_name="created_events")
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=False)
    start_date = models.DateTimeField(blank=False)
    end_date = models.DateTimeField(blank=False)
    attendees = models.ManyToManyField(
        Profile, related_name="attending_events", blank=True
    )
    location = models.CharField(max_length=255, blank=False)
    city = models.ForeignKey(City, models.CASCADE, blank=False)
    canceled = models.BooleanField(default=False)

    def __str__(self):
        return self.title


@receiver(
    post_save, sender=Event, dispatch_uid="event_author_is_automatically_an_attendee"
)
def event_author_is_automatically_an_attendee(sender, instance, created, **kwargs):
    if not created:
        return

    event = instance
    event.attendees.add(event.author)
    event.save()
