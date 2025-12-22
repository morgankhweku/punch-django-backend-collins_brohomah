from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password

from .models import PasswordResetCode
from .serializers import (
    RequestResetSerializer,
    VerifyCodeSerializer,
    ResetPasswordSerializer
)
from .utils import generate_otp, send_reset_email

User = get_user_model()


class RequestPasswordResetView(APIView):
    """
    Step 1:
    User provides email.
    We generate an OTP, hash it, store it, and send it via email.
    """

    def post(self, request):
        serializer = RequestResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Prevent email enumeration
            return Response(
                {"detail": "If the account exists, a reset code has been sent."},
                status=status.HTTP_200_OK
            )

        # Generate OTP
        code = generate_otp()

        # Store hashed OTP
        PasswordResetCode.objects.create(
            user=user,
            code=make_password(code)
        )

        # Send email
        send_reset_email(user.email, code)

        return Response(
            {"detail": "Verification code sent."},
            status=status.HTTP_200_OK
        )


class VerifyResetCodeView(APIView):
    """
    Step 2:
    User submits email + OTP.
    We verify OTP correctness and expiry.
    """

    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]

        try:
            reset = PasswordResetCode.objects.filter(
                user__email=email,
                is_used=False
            ).latest("created_at")
        except PasswordResetCode.DoesNotExist:
            return Response(
                {"detail": "Invalid verification code."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if reset.is_expired():
            return Response(
                {"detail": "Verification code has expired."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not check_password(code, reset.code):
            return Response(
                {"detail": "Invalid verification code."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"detail": "Verification successful."},
            status=status.HTTP_200_OK
        )


class ResetPasswordView(APIView):
    """
    Step 3:
    User submits email + OTP + new password.
    We verify OTP again, reset password, and invalidate OTP.
    """

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]
        password = serializer.validated_data["password"]

        try:
            reset = PasswordResetCode.objects.filter(
                user__email=email,
                is_used=False
            ).latest("created_at")
        except PasswordResetCode.DoesNotExist:
            return Response(
                {"detail": "Invalid verification code."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if reset.is_expired():
            return Response(
                {"detail": "Verification code has expired."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not check_password(code, reset.code):
            return Response(
                {"detail": "Invalid verification code."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Reset password
        user = reset.user
        user.set_password(password)
        user.save()

        # Invalidate OTP
        reset.is_used = True
        reset.save()

        return Response(
            {"detail": "Password reset successful."},
            status=status.HTTP_200_OK
        )
