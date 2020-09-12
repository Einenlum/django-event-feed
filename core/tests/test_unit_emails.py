from django.core.mail.message import EmailMessage
from core.email_backends import MailJetBackend


def test_backend_creates_accurate_email_message_format_from_django_email_message():
    backend = MailJetBackend()
    email_message = EmailMessage(
        subject="Some subject",
        body="Some body",
        from_email="john@john.com",
        to=("pierre@pierre.com",),
    )

    assert backend._build_message(email_message) == {
        "From": {"Email": "john@john.com"},
        "To": [{"Email": "pierre@pierre.com"}],
        "Subject": "Some subject",
        "HTMLPart": "Some body",
    }
