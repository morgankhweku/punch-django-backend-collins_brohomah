import secrets
from django.core.mail import send_mail
from django.conf import settings


def generate_otp():
    return str(secrets.randbelow(900000) + 100000)


def send_reset_email(email, code):
    send_mail(
        subject="Password Reset Code",
        message=f"Your password reset code is {code}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
