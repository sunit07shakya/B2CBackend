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
from .serializers.account_serializer import CustomTokenObtainPairSerializer


# Login API
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
