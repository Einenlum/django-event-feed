from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage, sanitize_address
from mailjet_rest import Client

from eventfeed.settings import MAILJET_API_KEY, MAILJET_API_SECRET


class MailJetBackend(BaseEmailBackend):
    def __init__(self, fail_silently=True, **kwargs):
        self._fail_silently = fail_silently
        self._client = Client(
            auth=(settings.MAILJET_API_KEY, settings.MAILJET_API_SECRET), version="v3.1"
        )

    def send_messages(self, email_messages):
        messages_with_recipients = [
            email_message
            for email_message in email_messages
            if email_message.recipients()
        ]
        messages = [
            self._build_message(message) for message in messages_with_recipients
        ]
        data = {"Messages": messages}

        try:
            response = self._client.send.create(data=data)
        except Client.ApiError:
            if not self._fail_silently:
                raise

        return len(messages)

    def _build_message(self, email_message: EmailMessage):
        encoding = email_message.encoding or settings.DEFAULT_CHARSET
        from_email = sanitize_address(email_message.from_email, encoding)
        recipients = [
            sanitize_address(addr, encoding) for addr in email_message.recipients()
        ]

        data = {
            "From": {"Email": from_email},
            "To": [{"Email": email} for email in recipients],
            "Subject": email_message.subject,
            "HTMLPart": email_message.body,
        }

        return data
