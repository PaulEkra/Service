from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import OTP
import random
from rest_framework.permissions import AllowAny


def send_otp_email(email, otp_code):
    subject = 'Votre code OTP'
    message = f'Votre code OTP est : {otp_code}'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


class GenerateOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        otp, created = OTP.objects.get_or_create(email=email)
        if not created:
            otp.delete()
            otp = OTP(email=email)

        otp.code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        otp.save()

        # Send the OTP to the email
        send_otp_email(otp.email, otp.code)

        return Response({"message": "OTP generated and sent to email"}, status=status.HTTP_201_CREATED)

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        if not email or not code:
            return Response({"error": "Email and code are required"}, status=status.HTTP_400_BAD_REQUEST)

        otp = get_object_or_404(OTP, email=email)

        if otp.code == code:
            return Response({"verified": True}, status=status.HTTP_200_OK)
        else:
            return Response({"verified": False}, status=status.HTTP_400_BAD_REQUEST)