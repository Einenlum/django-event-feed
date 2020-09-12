from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from core.models import Event, Profile


@shared_task
def notify_author_that_a_new_profile_attends_their_event(event_pk, attendee_pk):
    event = Event.objects.get(pk=event_pk)
    attendee = Profile.objects.get(pk=attendee_pk)
    author_email = event.author.user.email
    if not author_email:
        return

    args = {
        "event_title": event.title,
        "attendee_name": str(attendee),
        "author_name": str(event.author),
        "num_attendees": event.attendees.count(),
    }
    body = """
    <h1>Another person coming to your party!</h1>

    <p>Hi {author_name}!</p>

    <p>We heard something cool… wanna know?! We heard that {attendee_name} plans to come to your event! Yay!</p>
    <p>This gives us <b>{num_attendees}</b> for now! How cool is that?</p>

    <p>See you soon!</p>
    """.format(
        **args
    )

    send_mail(
        subject="Hey! Someone new is coming!",
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[author_email],
    )
