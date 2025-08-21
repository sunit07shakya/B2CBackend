# users/serializers.py

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# For Login API
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # You can add more custom claims here

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({'user':{
            'id':self.user.id,
            'username':self.user.username,
            'email':self.user.email,
            'first_name':self.user.first_name,
            'last_name':self.user.last_name
        }})
        return data
       
