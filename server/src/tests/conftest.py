import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from decimal import Decimal
from datetime import datetime, timedelta

from apps.core.models import ParkingLot, Booking

User = get_user_model()

@pytest.fixture
def user():
    return User.objects.create_user(
        email='testuser@example.com',
        username='testuser',
        password='testpassword123',
        first_name='Test',
        last_name='User'
    )

@pytest.fixture
def owner():
    return User.objects.create_user(
        email='owner@example.com',
        username='spotowner',
        password='ownerpass123',
        first_name='Spot',
        last_name='Owner'
    )

@pytest.fixture
def parking_spot(owner):
    return ParkingLot.objects.create(
        owner=owner,
        title='Test Parking Spot',
        description='A great parking spot',
        address='123 Test St, Test City',
        latitude=Decimal('37.7749'),
        longitude=Decimal('-122.4194'),
        spot_type='garage',
        price_per_hour=Decimal('15.00'),
        availability='24_7'
    )

@pytest.fixture
def authenticated_client(user):
    client = APIClient()
    token = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')
    return client

@pytest.fixture
def booking(user, parking_spot):
    return Booking.objects.create(
        user=user,
        spot=parking_spot,
        start_time=datetime.now() + timedelta(hours=1),
        end_time=datetime.now() + timedelta(hours=3),
        duration_hours=2,
        total_price=Decimal('30.00'),
        status='confirmed'
    )
