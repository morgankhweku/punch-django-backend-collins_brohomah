from django.urls import path
from .views import (
    RequestPasswordResetView,
    VerifyResetCodeView,
    ResetPasswordView
)

urlpatterns = [
    path("request", RequestPasswordResetView.as_view()),
    path("verify", VerifyResetCodeView.as_view()),
    path("reset/", ResetPasswordView.as_view()),
]
