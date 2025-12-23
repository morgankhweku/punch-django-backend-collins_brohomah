from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
import logging

from .serializers import RegisterSerializer
from .services import authenticate_user


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ValidationError as e:
            logging.error(f"Registration validation error: {e.detail}")
            raise

        return Response(
            {"message": "User registered successfully"},
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate_user(email=email, password=password)

        if user is None:
            return Response(
                {"error": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                },
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK
        )


class SessionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "authenticated": True,
                "user": {
                    "id": request.user.id,
                    "email": request.user.email,
                    "username": request.user.username,
                },
            },
            status=status.HTTP_200_OK
        )
