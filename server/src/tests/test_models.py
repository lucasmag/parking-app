import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import datetime, timedelta

from apps.core.models import ParkingLot, Booking, Review, FavoriteSpot

User = get_user_model()

@pytest.mark.django_db
class TestParkingLotModel:
    
    def test_parking_spot_creation(self, owner):
        spot = ParkingLot.objects.create(
            owner=owner,
            title='Test Spot',
            address='123 Test St',
            latitude=Decimal('37.7749'),
            longitude=Decimal('-122.4194'),
            spot_type='garage',
            price_per_hour=Decimal('15.00'),
            availability='24_7'
        )
        
        assert str(spot) == 'Test Spot - 123 Test St'
        assert spot.rating == 0.0
        assert spot.is_active is True

    def test_parking_spot_features(self, owner):
        features = ['covered', 'security', 'ev_charging']
        spot = ParkingLot.objects.create(
            owner=owner,
            title='Featured Spot',
            address='456 Feature Ave',
            latitude=Decimal('37.7849'),
            longitude=Decimal('-122.4094'),
            spot_type='lot',
            price_per_hour=Decimal('12.00'),
            availability='weekdays_9_5',
            features=features
        )
        
        assert spot.features == features

@pytest.mark.django_db
class TestBookingModel:
    
    def test_booking_creation(self, user, parking_spot):
        start_time = datetime.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        
        booking = Booking.objects.create(
            user=user,
            spot=parking_spot,
            start_time=start_time,
            end_time=end_time,
            duration_hours=2,
            total_price=Decimal('30.00')
        )
        
        assert booking.booking_id is not None
        assert booking.booking_id.startswith('BK')
        assert booking.status == 'pending'
        assert str(booking).endswith(user.email)

    def test_booking_qr_code_generation(self, user, parking_spot):
        start_time = datetime.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        
        booking = Booking.objects.create(
            user=user,
            spot=parking_spot,
            start_time=start_time,
            end_time=end_time,
            duration_hours=2,
            total_price=Decimal('30.00')
        )
        
        assert booking.qr_code is not None
        assert 'qr_code_' in booking.qr_code.name

@pytest.mark.django_db 
class TestReviewModel:
    
    def test_review_creation(self, user, parking_spot, booking):
        review = Review.objects.create(
            user=user,
            spot=parking_spot,
            booking=booking,
            rating=5,
            comment='Great spot!'
        )
        
        assert str(review) == f'5 stars - {parking_spot.title}'
        assert review.rating == 5

@pytest.mark.django_db
class TestFavoriteSpotModel:
    
    def test_favorite_spot_creation(self, user, parking_spot):
        favorite = FavoriteSpot.objects.create(
            user=user,
            spot=parking_spot
        )
        
        assert str(favorite) == f'{user.email} - {parking_spot.title}'
