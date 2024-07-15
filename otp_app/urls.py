from django.urls import path
from .views import GenerateOTPView, VerifyOTPView

urlpatterns = [
    path('generate/', GenerateOTPView.as_view(), name='generate-otp'),
    path('verify/', VerifyOTPView.as_view(), name='verify-otp'),
]
