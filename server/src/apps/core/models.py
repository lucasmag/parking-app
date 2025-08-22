from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django.db import models
from apps.common.models import BaseModel
from django.core.validators import MinValueValidator
import uuid
from django.contrib.auth import get_user_model


User = get_user_model()


class BookingStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CONFIRMED = 'confirmed', 'Confirmed'
    ACTIVE = 'active', 'Active'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'
    EXPIRED = 'expired', 'Expired'


class ParkingLotTypes(models.TextChoices):
    GARAGE = 'garage', 'Parking Garage'
    LOT = 'lot', 'Parking Lot'
    STREET = 'street', 'Street Parking'
    DRIVEWAY = 'driveway', 'Private Driveway'
    OTHER = 'other', 'Other'


class ParkingLotAvailability(models.TextChoices):
    WEEKDAYS_9_5 = 'weekdays_9_5', 'Weekdays (9-5)'
    WEEKENDS = 'weekends', 'Weekends'
    TWENTY_FOUR_SEVEN = '24_7', '24/7'
    CUSTOM = 'custom', 'Custom Hours'


class ParkingLot(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_spots')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    address = models.TextField()
    location = gis_models.PointField(srid=4326)  # WGS84 coordinate system
    
    # Keep these for backwards compatibility and easy access
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    
    spot_type = models.CharField(max_length=20, choices=ParkingLotTypes.choices, default=ParkingLotTypes.OTHER)
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    available_spots = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    availability = models.CharField(max_length=20, choices=ParkingLotAvailability.choices)
    features = models.JSONField(default=list, blank=True)  # ['covered', 'security', 'ev_charging']
    instructions = models.TextField(blank=True)

    class Meta:
        db_table = 'parking_lot'
        indexes = [
            # PostGIS automatically creates spatial indexes, but we can be explicit
            gis_models.Index(fields=['location']),
        ]

    def save(self, *args, **kwargs):
        if self.latitude and self.longitude:
            self.location = Point(float(self.longitude), float(self.latitude))
        # Extract lat/lng from Point if location is set but lat/lng are None
        elif self.location and not (self.latitude and self.longitude):
            self.longitude = self.location.x
            self.latitude = self.location.y
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.address}"


class Booking(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking_id = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking')
    spot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE, related_name='booking')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_hours = models.DecimalField(max_digits=4, decimal_places=2)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=BookingStatus, default='pending')
    payment_intent_id = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'booking'
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['spot', 'start_time', 'end_time']),
        ]

    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = self.generate_booking_id()
        super().save(*args, **kwargs)

    def generate_booking_id(self):
        import random
        return f"BK{random.randint(100, 999)}-{random.randint(10000, 99999)}"

    def __str__(self):
        return f"Booking {self.booking_id} - {self.user.email}"