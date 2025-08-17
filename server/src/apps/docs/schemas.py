"""
API Documentation Schemas
Centralized location for all API response/request schemas
"""
from rest_framework import serializers
from apps.user.serializers import UserProfileSerializer

# User Authentication Schemas
class UserAuthResponseSchema(serializers.Serializer):
    """Schema for authentication response"""
    message = serializers.CharField()
    user = UserProfileSerializer()
    refresh = serializers.CharField()
    access = serializers.CharField()

class LogoutRequestSchema(serializers.Serializer):
    """Schema for logout request"""
    refresh = serializers.CharField(help_text="Refresh token to blacklist")

class LogoutResponseSchema(serializers.Serializer):
    """Schema for logout response"""
    message = serializers.CharField()

class ProtectedResponseSchema(serializers.Serializer):
    """Schema for protected endpoint response"""
    message = serializers.CharField()
    user_id = serializers.IntegerField()
    username = serializers.CharField()

class PasswordChangeResponseSchema(serializers.Serializer):
    """Schema for password change response"""
    message = serializers.CharField()

# Booking Schemas
class BookingsResponseSchema(serializers.Serializer):
    """Schema for bookings response"""
    bookings = serializers.ListField(
        child=serializers.DictField(
            child=serializers.DateTimeField()
        )
    )

class ExtendSessionRequestSchema(serializers.Serializer):
    """Schema for extend session request"""
    hours = serializers.FloatField(help_text="Number of hours to extend", default=1)

class ExtendSessionResponseSchema(serializers.Serializer):
    """Schema for extend session response"""
    message = serializers.CharField()
    new_end_time = serializers.DateTimeField()
    additional_cost = serializers.DecimalField(max_digits=8, decimal_places=2)
    total_price = serializers.DecimalField(max_digits=8, decimal_places=2)

class CancelBookingResponseSchema(serializers.Serializer):
    """Schema for cancel booking response"""
    message = serializers.CharField()

# Parking Lot Schemas
class ParkingLotAvailabilityResponseSchema(serializers.Serializer):
    """Schema for parking lot availability response"""
    spot_id = serializers.UUIDField()
    date = serializers.DateField()
    booked_slots = serializers.ListField(
        child=serializers.DictField(
            child=serializers.DateTimeField()
        )
    )

# Dashboard Schemas
class UserStatsSchema(serializers.Serializer):
    """Schema for user statistics"""
    total_bookings = serializers.IntegerField()
    active_bookings = serializers.IntegerField()
    upcoming_bookings = serializers.IntegerField()

class OwnerStatsSchema(serializers.Serializer):
    """Schema for owner statistics"""
    owned_spots = serializers.IntegerField()
    total_earnings = serializers.DecimalField(max_digits=10, decimal_places=2)

class DashboardStatsResponseSchema(serializers.Serializer):
    """Schema for dashboard stats response"""
    user_stats = UserStatsSchema()
    owner_stats = OwnerStatsSchema()

# Search Schemas
class SearchResultsSchema(serializers.Serializer):
    """Schema for search results"""
    count = serializers.IntegerField()
    results = serializers.ListField()  # Will be populated with ParkingLotListSerializer

# Error Schemas
class ErrorResponseSchema(serializers.Serializer):
    """Standard error response schema"""
    error = serializers.CharField()

class ValidationErrorResponseSchema(serializers.Serializer):
    """Validation error response schema"""
    field_errors = serializers.DictField()
    non_field_errors = serializers.ListField(child=serializers.CharField(), required=False)