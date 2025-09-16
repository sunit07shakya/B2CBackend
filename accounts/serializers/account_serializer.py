import random
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.timezone import make_aware
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import CustomUser
from marketplace.utils import merge_guest_cart


class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        request = self.context["request"]
        email = validated_data["email"]

        otp = random.randint(100000, 999999)

        # Store OTP in session
        request.session["email_otp"] = otp
        request.session["otp_email"] = email
        request.session["otp_expiry"] = (timezone.now() + timezone.timedelta(minutes=5)).isoformat()

        # --- Email sending logic ---
        subject = "Your Login OTP"
        message = f"Your OTP for login is {otp}. It is valid for 5 minutes."
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        except Exception as e:
            raise serializers.ValidationError(f"Failed to send OTP email: {str(e)}")

        return {"message": "OTP sent successfully","otp":otp}  # Include OTP for testing purposes  


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(required=False, write_only=True)
    otp = serializers.CharField(required=False, write_only=True)

    def validate(self, data):
        request = self.context["request"]
        email = data.get("email")
        password = data.get("password")
        otp = data.get("otp")

        user = None

        # Case 1: Email + Password
        if password:
            user = authenticate(request, username=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials")

        # Case 2: Email + OTP
        elif otp:
            session_email = request.session.get("otp_email")
            session_otp = request.session.get("email_otp")
            session_expiry = request.session.get("otp_expiry")

            if not session_email or not session_otp:
                raise serializers.ValidationError("OTP not requested")

            if session_email != email or str(session_otp) != str(otp):
                raise serializers.ValidationError("Invalid OTP")

            # expiry = make_aware(datetime.fromisoformat(session_expiry))
            # if timezone.now() > expiry:
            #     raise serializers.ValidationError("OTP expired")
            expiry_dt = datetime.fromisoformat(session_expiry)  # could be aware already

            if timezone.is_naive(expiry_dt):
                expiry_dt = timezone.make_aware(expiry_dt)

            if timezone.now() > expiry_dt:
                raise serializers.ValidationError("OTP expired")
            # If user doesn’t exist → create
            user, created = CustomUser.objects.get_or_create(
                email=email,
                defaults={"username": email.split("@")[0]}
            )

        else:
            raise serializers.ValidationError("Provide either password or OTP")

         # 🔥 Merge guest cart into user's cart
        merge_guest_cart(user, request)
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
            }
        }
