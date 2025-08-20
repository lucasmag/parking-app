import factory
from factory.django import DjangoModelFactory
from factory import Faker, SubFactory
from django.contrib.auth import get_user_model
from apps.core.models import ParkingLot, Booking, BookingStatus, ParkingLotTypes, ParkingLotAvailability
from datetime import datetime, timedelta
from decimal import Decimal
import random

User = get_user_model()


class UserFactory(DjangoModelFactory):
    """Factory for User model"""

    class Meta:
        model = User

    email = Faker("email")
    username = Faker("user_name")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    is_verified = True
    phone_number = Faker("phone_number")

    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        """Set password after creation"""
        if not create:
            return
        password = extracted or "testpass123"
        obj.set_password(password)
        obj.save()


class ParkingLotFactory(DjangoModelFactory):
    """Factory for ParkingLot model"""

    class Meta:
        model = ParkingLot

    owner = SubFactory(UserFactory)
    title = Faker("company")
    description = Faker("text", max_nb_chars=200)
    address = Faker("address")

    # Generate coordinates around major cities
    latitude = Faker(
        "pydecimal",
        left_digits=2,
        right_digits=6,
        min_value=Decimal("25.0"),
        max_value=Decimal("49.0"),
    )
    longitude = Faker(
        "pydecimal",
        left_digits=3,
        right_digits=6,
        min_value=Decimal("-125.0"),
        max_value=Decimal("-66.0"),
    )

    spot_type = Faker(
        "random_element", elements=[choice[0] for choice in ParkingLotTypes.choices]
    )
    price_per_hour = Faker(
        "pydecimal",
        left_digits=2,
        right_digits=2,
        min_value=Decimal("1.00"),
        max_value=Decimal("25.00"),
    )
    available_spots = Faker("random_int", min=1, max=50)
    availability = Faker(
        "random_element",
        elements=[choice[0] for choice in ParkingLotAvailability.choices],
    )

    @factory.lazy_attribute
    def features(self):
        """Generate random features"""
        possible_features = [
            "covered",
            "security",
            "ev_charging",
            "wheelchair_accessible",
            "valet",
            "24_7_access",
            "car_wash",
            "surveillance",
        ]
        return random.sample(possible_features, random.randint(0, 4))

    instructions = Faker("text", max_nb_chars=100)


class BookingFactory(DjangoModelFactory):
    """Factory for Booking model"""

    class Meta:
        model = Booking

    user = SubFactory(UserFactory)
    spot = SubFactory(ParkingLotFactory)

    @factory.lazy_attribute
    def start_time(self):
        """Generate future start time"""
        base_time = datetime.now() + timedelta(hours=random.randint(1, 48))
        return base_time.replace(minute=0, second=0, microsecond=0)

    @factory.lazy_attribute
    def end_time(self):
        """Generate end time based on start time"""
        duration_hours = random.randint(1, 8)
        return self.start_time + timedelta(hours=duration_hours)

    @factory.lazy_attribute
    def duration_hours(self):
        """Calculate duration based on start and end times"""
        duration = self.end_time - self.start_time
        return Decimal(str(duration.total_seconds() / 3600))

    @factory.lazy_attribute
    def total_price(self):
        """Calculate total price based on duration and spot price"""
        return self.duration_hours * self.spot.price_per_hour

    status = Faker(
        "random_element", elements=[choice[0] for choice in BookingStatus.choices]
    )
    notes = Faker("text", max_nb_chars=100)


# ======= Specialized factories for specific test scenarios =======


class NYCParkingLotFactory(ParkingLotFactory):
    """Factory for NYC-based parking lots"""

    latitude = Faker(
        "pydecimal",
        left_digits=2,
        right_digits=6,
        min_value=Decimal("40.6"),
        max_value=Decimal("40.9"),
    )
    longitude = Faker(
        "pydecimal",
        left_digits=3,
        right_digits=6,
        min_value=Decimal("-74.3"),
        max_value=Decimal("-73.7"),
    )
    address = factory.LazyAttribute(
        lambda: f"{Faker().street_address()}, New York, NY"
    )


class ExpensiveParkingLotFactory(ParkingLotFactory):
    """Factory for expensive parking lots"""

    price_per_hour = Faker(
        "pydecimal",
        left_digits=2,
        right_digits=2,
        min_value=Decimal("15.00"),
        max_value=Decimal("50.00"),
    )
    features = ["valet", "security", "covered"]


class CheapParkingLotFactory(ParkingLotFactory):
    """Factory for cheap parking lots"""

    price_per_hour = Faker(
        "pydecimal",
        left_digits=1,
        right_digits=2,
        min_value=Decimal("1.00"),
        max_value=Decimal("5.00"),
    )


class ActiveBookingFactory(BookingFactory):
    """Factory for active bookings"""

    status = BookingStatus.ACTIVE

    @factory.lazy_attribute
    def start_time(self):
        """Active booking started in the past"""
        return datetime.now() - timedelta(hours=random.randint(1, 4))


class CompletedBookingFactory(BookingFactory):
    """Factory for completed bookings"""

    status = BookingStatus.COMPLETED

    @factory.lazy_attribute
    def start_time(self):
        """Completed booking in the past"""
        return datetime.now() - timedelta(days=random.randint(1, 30))

    @factory.lazy_attribute
    def end_time(self):
        """End time also in the past"""
        return self.start_time + timedelta(hours=random.randint(1, 8))


class FutureBookingFactory(BookingFactory):
    """Factory for future bookings"""

    status = BookingStatus.CONFIRMED

    @factory.lazy_attribute
    def start_time(self):
        """Future booking"""
        return datetime.now() + timedelta(days=random.randint(1, 30))
