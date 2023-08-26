from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
import random


def random_code():
    return random.randint(100000, 999999)


def send_confirmation_email(request, email, code):
    url = f'/email-confirmation/'
    text = render_to_string('confirmation_code.html', {'email': email, 'code': code}, request)
    send_mail(
        subject=_("Email Confirmation"),
        message=text,
        html_message=text,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )
