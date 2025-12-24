import secrets
from django.core.mail import send_mail
from django.conf import settings


def generate_otp():
    return str(secrets.randbelow(900000) + 100000)


def send_reset_email(email, code):
    subject = "Password Reset Code - PunchChat"
    message = f"""
Hello,

You have requested to reset your password for your PunchChat account.

Your verification code is: {code}

This code will expire in 10 minutes for security reasons.

If you did not request this password reset, please ignore this email.

Best regards,
PunchChat Team
"""

    html_message = f"""
    <html>
    <body>
        <h2>Password Reset Request</h2>
        <p>Hello,</p>
        <p>You have requested to reset your password for your PunchChat account.</p>
        <div style="background-color: #f0f0f0; padding: 20px; margin: 20px 0; border-radius: 5px;">
            <h3 style="color: #333; margin: 0;">Your verification code is:</h3>
            <h1 style="color: #007bff; font-size: 32px; margin: 10px 0;">{code}</h1>
        </div>
        <p><strong>This code will expire in 10 minutes</strong> for security reasons.</p>
        <p>If you did not request this password reset, please ignore this email.</p>
        <br>
        <p>Best regards,<br>PunchChat Team</p>
    </body>
    </html>
    """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
        html_message=html_message,
    )
