# users/urls.py

from django.urls import path
from .views.auth_view import (SendOTPView, LoginAPIView)
from .views.address_view import AddressListCreateView, AddressUpdateDeleteView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),

    # Address management endpoints
    path("addresses/", AddressListCreateView.as_view(), name="address-list-create"),
    path("addresses/<int:pk>/", AddressUpdateDeleteView.as_view(), name="address-update-delete"),

]