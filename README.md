# Django Event Feed

You can see the API in action [here on Heroku](https://django-event-feed.herokuapp.com/doc/).

A toy project to play with Django Rest Framework.
Only the REST API is coded. No frontend.

Users can create an event (like in Meetup or Eventbrite), delete or edit their events.
Anonymous users can list all the events.
Registered users can also get the detail of an event and see who is attending it.

## Stack

* Django REST Framework
* pytest + pytest-xdist (for parallel testing)
* drf-yasg (to generate documentation)
* django-guardian (to use object permissions)
* black (opinonated linter)
* Emails are sent through MailJet, thanks to [a custom EmailBackend](core/email_backends.py)
* Email sending is asynchronous thanks to Celery

## Tests

In one term:

```bash
make celery_test
```

In another one:

```bash
make test
```
