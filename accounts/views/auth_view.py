# accounts/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import generics
from django.contrib.auth import login
from django_filters.rest_framework import DjangoFilterBackend

# views
from rest_framework_simplejwt.views import TokenObtainPairView

# serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..serializers.account_serializer import SendOTPSerializer, LoginSerializer


class SendOTPView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response(result, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
