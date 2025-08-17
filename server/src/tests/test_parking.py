import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta
from decimal import Decimal

from apps.core.models import ParkingLot, Booking, Review, FavoriteSpot

User = get_user_model()

class ParkingLotTestCase(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )
        self.owner = User.objects.create_user(
            email='owner@example.com',
            username='spotowner',
            password='ownerpass123',
            first_name='Spot',
            last_name='Owner'
        )
        
        # Create parking spot
        self.spot = ParkingLot.objects.create(
            owner=self.owner,
            title='Test Parking Spot',
            description='A great parking spot',
            address='123 Test St, Test City',
            latitude=Decimal('37.7749'),
            longitude=Decimal('-122.4194'),
            spot_type='garage',
            price_per_hour=Decimal('15.00'),
            availability='24_7'
        )
        
        # Authenticate user
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')

    def test_list_parking_spots(self):
        """Test listing parking spots"""
        response = self.client.get('/api/parking-spots/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_parking_spot_detail(self):
        """Test getting parking spot details"""
        response = self.client.get(f'/api/parking-spots/{self.spot.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.spot.title)

    def test_search_parking_spots_by_location(self):
        """Test searching parking spots by location"""
        response = self.client.get('/api/search/', {
            'lat': 37.7749,
            'lng': -122.4194,
            'start_time': (datetime.now() + timedelta(hours=1)).isoformat(),
            'end_time': (datetime.now() + timedelta(hours=3)).isoformat(),
            'radius': 10
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_toggle_favorite_spot(self):
        """Test toggling favorite spot"""
        response = self.client.post(f'/api/parking-spots/{self.spot.id}/toggle_favorite/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['favorited'])
        
        # Toggle again to unfavorite
        response = self.client.post(f'/api/parking-spots/{self.spot.id}/toggle_favorite/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['favorited'])

    def test_create_parking_spot(self):
        """Test creating a new parking spot"""
        spot_data = {
            'title': 'New Parking Spot',
            'description': 'Another great spot',
            'address': '456 Another St, Test City',
            'latitude': 37.7849,
            'longitude': -122.4094,
            'spot_type': 'lot',
            'price_per_hour': 12.00,
            'availability': 'weekdays_9_5',
            'features': ['covered', 'security']
        }
        
        response = self.client.post('/api/parking-spots/', spot_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ParkingLot.objects.count(), 2)

class BookingTestCase(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )
        self.owner = User.objects.create_user(
            email='owner@example.com',
            username='spotowner',
            password='ownerpass123',
            first_name='Spot',
            last_name='Owner'
        )
        
        self.spot = ParkingLot.objects.create(
            owner=self.owner,
            title='Test Parking Spot',
            address='123 Test St, Test City',
            latitude=Decimal('37.7749'),
            longitude=Decimal('-122.4194'),
            spot_type='garage',
            price_per_hour=Decimal('15.00'),
            availability='24_7'
        )
        
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')

    def test_create_booking(self):
        """Test creating a new booking"""
        start_time = datetime.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        
        booking_data = {
            'spot': str(self.spot.id),
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'duration_hours': 2,
            'notes': 'Test booking'
        }
        
        response = self.client.post('/api/bookings/', booking_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        
        booking = Booking.objects.first()
        self.assertEqual(booking.total_price, Decimal('30.00'))  # 2 hours * $15

    def test_create_overlapping_booking(self):
        """Test creating overlapping booking should fail"""
        start_time = datetime.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        
        # Create first booking
        Booking.objects.create(
            user=self.user,
            spot=self.spot,
            start_time=start_time,
            end_time=end_time,
            duration_hours=2,
            total_price=Decimal('30.00'),
            status='confirmed'
        )
        
        # Try to create overlapping booking
        overlap_start = start_time + timedelta(minutes=30)
        overlap_end = end_time + timedelta(minutes=30)
        
        booking_data = {
            'spot': str(self.spot.id),
            'start_time': overlap_start.isoformat(),
            'end_time': overlap_end.isoformat(),
            'duration_hours': 2
        }
        
        response = self.client.post('/api/bookings/', booking_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_extend_session(self):
        """Test extending an active booking session"""
    def test_cancel_booking(self):
        """Test cancelling a booking"""
        booking = Booking.objects.create(
            user=self.user,
            spot=self.spot,
            start_time=datetime.now() + timedelta(hours=1),
            end_time=datetime.now() + timedelta(hours=3),
            duration_hours=2,
            total_price=Decimal('30.00'),
            status='confirmed'
        )
        
        response = self.client.post(f'/api/bookings/{booking.id}/cancel_booking/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'cancelled')

    def test_list_user_bookings(self):
        """Test listing user's bookings"""
        Booking.objects.create(
            user=self.user,
            spot=self.spot,
            start_time=datetime.now() + timedelta(hours=1),
            end_time=datetime.now() + timedelta(hours=3),
            duration_hours=2,
            total_price=Decimal('30.00')
        )
        
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

class ReviewTestCase(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )
        self.owner = User.objects.create_user(
            email='owner@example.com',
            username='spotowner',
            password='ownerpass123',
            first_name='Spot',
            last_name='Owner'
        )
        
        self.spot = ParkingLot.objects.create(
            owner=self.owner,
            title='Test Parking Spot',
            address='123 Test St, Test City',
            latitude=Decimal('37.7749'),
            longitude=Decimal('-122.4194'),
            spot_type='garage',
            price_per_hour=Decimal('15.00'),
            availability='24_7'
        )
        
        self.booking = Booking.objects.create(
            user=self.user,
            spot=self.spot,
            start_time=datetime.now() - timedelta(hours=3),
            end_time=datetime.now() - timedelta(hours=1),
            duration_hours=2,
            total_price=Decimal('30.00'),
            status='completed'
        )
        
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')

    def test_create_review(self):
        """Test creating a review"""
        review_data = {
            'booking': str(self.booking.id),
            'rating': 5,
            'comment': 'Great parking spot!'
        }
        
        response = self.client.post('/api/reviews/', review_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)

    def test_create_duplicate_review(self):
        """Test creating duplicate review should fail"""
        Review.objects.create(
            user=self.user,
            spot=self.spot,
            booking=self.booking,
            rating=5,
            comment='First review'
        )
        
        review_data = {
            'booking': str(self.booking.id),
            'rating': 4,
            'comment': 'Second review'
        }
        
        response = self.client.post('/api/reviews/', review_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_spot_reviews(self):
        """Test listing reviews for a specific spot"""
        Review.objects.create(
            user=self.user,
            spot=self.spot,
            booking=self.booking,
            rating=5,
            comment='Great spot!'
        )
        
        response = self.client.get(f'/api/reviews/?spot_id={self.spot.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
