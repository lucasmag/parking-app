# apps/docs/parameters.py
"""
API Documentation Parameters
Centralized location for all API parameters
"""
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes

# Location Parameters
LATITUDE_PARAM = OpenApiParameter(
    name='lat',
    type=OpenApiTypes.FLOAT,
    location=OpenApiParameter.QUERY,
    description='Latitude coordinate for location-based search',
    required=True
)

LONGITUDE_PARAM = OpenApiParameter(
    name='lng',
    type=OpenApiTypes.FLOAT,
    location=OpenApiParameter.QUERY,
    description='Longitude coordinate for location-based search',
    required=True
)

RADIUS_PARAM = OpenApiParameter(
    name='radius',
    type=OpenApiTypes.FLOAT,
    location=OpenApiParameter.QUERY,
    description='Search radius in kilometers',
    default=10
)

# Time Parameters
START_TIME_PARAM = OpenApiParameter(
    name='start_time',
    type=OpenApiTypes.DATETIME,
    location=OpenApiParameter.QUERY,
    description='Start time for availability check (ISO format)',
    required=True
)

END_TIME_PARAM = OpenApiParameter(
    name='end_time',
    type=OpenApiTypes.DATETIME,
    location=OpenApiParameter.QUERY,
    description='End time for availability check (ISO format)',
    required=True
)

DATE_PARAM = OpenApiParameter(
    name='date',
    type=OpenApiTypes.DATE,
    location=OpenApiParameter.QUERY,
    description='Date to check availability (YYYY-MM-DD format)',
    default='today'
)

# Filter Parameters
MIN_PRICE_PARAM = OpenApiParameter(
    name='min_price',
    type=OpenApiTypes.FLOAT,
    location=OpenApiParameter.QUERY,
    description='Minimum price per hour filter'
)

MAX_PRICE_PARAM = OpenApiParameter(
    name='max_price',
    type=OpenApiTypes.FLOAT,
    location=OpenApiParameter.QUERY,
    description='Maximum price per hour filter'
)

SPOT_TYPE_PARAM = OpenApiParameter(
    name='spot_type',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description='Filter by parking spot type',
    enum=['garage', 'lot', 'street', 'driveway', 'other']
)

AVAILABILITY_PARAM = OpenApiParameter(
    name='availability',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description='Filter by availability schedule',
    enum=['weekdays_9_5', 'weekends', '24_7', 'custom']
)

# Search Parameters
SEARCH_PARAM = OpenApiParameter(
    name='search',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description='Search in title, address, and description'
)

# Ordering Parameters
ORDERING_PARAM = OpenApiParameter(
    name='ordering',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description='Order results by field (prefix with - for descending)',
    enum=['price_per_hour', '-price_per_hour', 'created_at', '-created_at', 'distance']
)

# Status Parameters
STATUS_PARAM = OpenApiParameter(
    name='status',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description='Filter bookings by status',
    enum=['pending', 'confirmed', 'active', 'completed', 'cancelled', 'expired']
)