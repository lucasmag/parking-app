# apps/docs/decorators.py
"""
API Documentation Decorators
Pre-configured decorators for consistent API documentation
"""
from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.docs.schemas import *
from apps.docs.parameters import *

# User Documentation Decorators
USER_VIEWSET_DOCS = extend_schema_view(
    list=extend_schema(
        summary="List users",
        description="List all users (admin only)",
        tags=["Users"]
    ),
    retrieve=extend_schema(
        summary="Get user details",
        description="Get user profile by ID or 'me' for current user",
        tags=["Users"]
    ),
    update=extend_schema(
        summary="Update user profile",
        description="Update user profile information",
        tags=["Users"]
    ),
    partial_update=extend_schema(
        summary="Partial update user profile",
        description="Partially update user profile information",
        tags=["Users"]
    ),
    destroy=extend_schema(
        summary="Delete user account",
        description="Delete user account (admin only)",
        tags=["Users"]
    ),
)

USER_REGISTER_DOCS = extend_schema(
    summary="Register new user",
    description="Create a new user account and return JWT tokens",
    responses={
        201: UserAuthResponseSchema,
        400: ValidationErrorResponseSchema
    },
    tags=["Authentication"],
    auth=[]
)

USER_LOGIN_DOCS = extend_schema(
    summary="User login",
    description="Authenticate user and return JWT tokens",
    responses={
        200: UserAuthResponseSchema,
        400: ValidationErrorResponseSchema
    },
    tags=["Authentication"],
    auth=[]
)

USER_LOGOUT_DOCS = extend_schema(
    summary="User logout",
    description="Logout user and blacklist refresh token",
    request=LogoutRequestSchema,
    responses={
        205: LogoutResponseSchema,
        400: ErrorResponseSchema
    },
    tags=["Authentication"]
)

USER_PROFILE_DOCS = extend_schema(
    summary="Get current user profile",
    description="Get authenticated user's profile information",
    responses={200: UserProfileSerializer},
    tags=["Users"]
)

USER_CHANGE_PASSWORD_DOCS = extend_schema(
    summary="Change password",
    description="Change the authenticated user's password",
    responses={
        200: PasswordChangeResponseSchema,
        400: ValidationErrorResponseSchema
    },
    tags=["Users"]
)

USER_PROTECTED_DOCS = extend_schema(
    summary="Protected endpoint",
    description="Example protected endpoint for testing authentication",
    responses={200: ProtectedResponseSchema},
    tags=["Testing"]
)

# Parking Lot Documentation Decorators
PARKING_LOT_VIEWSET_DOCS = extend_schema_view(
    list=extend_schema(
        summary="List parking lots",
        description="List available parking lots with optional location-based filtering",
        parameters=[LATITUDE_PARAM, LONGITUDE_PARAM, RADIUS_PARAM, SEARCH_PARAM, ORDERING_PARAM],
        tags=["Parking Lots"]
    ),
    create=extend_schema(
        summary="Create parking lot",
        description="Create a new parking lot listing",
        tags=["Parking Lots"]
    ),
    retrieve=extend_schema(
        summary="Get parking lot details",
        description="Get detailed information about a specific parking lot",
        tags=["Parking Lots"]
    ),
    update=extend_schema(
        summary="Update parking lot",
        description="Update parking lot information (owner only)",
        tags=["Parking Lots"]
    ),
    partial_update=extend_schema(
        summary="Partial update parking lot",
        description="Partially update parking lot information (owner only)",
        tags=["Parking Lots"]
    ),
    destroy=extend_schema(
        summary="Delete parking lot",
        description="Delete parking lot listing (owner only)",
        tags=["Parking Lots"]
    ),
)

PARKING_LOT_AVAILABILITY_DOCS = extend_schema(
    summary="Check parking lot availability",
    description="Get availability information for a specific parking lot on a given date",
    parameters=[DATE_PARAM],
    responses={200: ParkingLotAvailabilityResponseSchema},
    tags=["Parking Lots"]
)

# Booking Documentation Decorators
BOOKING_VIEWSET_DOCS = extend_schema_view(
    list=extend_schema(
        summary="List user bookings",
        description="List all bookings for the authenticated user",
        parameters=[STATUS_PARAM, ORDERING_PARAM],
        tags=["Bookings"]
    ),
    create=extend_schema(
        summary="Create booking",
        description="Create a new parking spot booking",
        tags=["Bookings"]
    ),
    retrieve=extend_schema(
        summary="Get booking details",
        description="Get detailed information about a specific booking",
        tags=["Bookings"]
    ),
    update=extend_schema(
        summary="Update booking",
        description="Update booking information",
        tags=["Bookings"]
    ),
    destroy=extend_schema(
        summary="Cancel booking",
        description="Cancel a booking",
        tags=["Bookings"]
    ),
)

BOOKING_EXTEND_SESSION_DOCS = extend_schema(
    summary="Extend booking session",
    description="Extend an active booking session by additional hours",
    request=ExtendSessionRequestSchema,
    responses={
        200: ExtendSessionResponseSchema,
        400: ErrorResponseSchema
    },
    tags=["Bookings"]
)

BOOKING_CANCEL_DOCS = extend_schema(
    summary="Cancel booking",
    description="Cancel a pending or confirmed booking",
    responses={
        200: CancelBookingResponseSchema,
        400: ErrorResponseSchema
    },
    tags=["Bookings"]
)

# My Parking Lots Documentation Decorators
MY_PARKING_LOTS_VIEWSET_DOCS = extend_schema_view(
    list=extend_schema(
        summary="List owned parking lots",
        description="List parking lots owned by the current user",
        tags=["My Parking Lots"]
    ),
    retrieve=extend_schema(
        summary="Get owned parking lot details",
        description="Get details of a parking lot owned by the current user",
        tags=["My Parking Lots"]
    ),
)

MY_PARKING_LOT_BOOKINGS_DOCS = extend_schema(
    summary="Get parking lot bookings",
    description="Get all bookings for a specific parking lot owned by the user",
    responses={200: BookingsResponseSchema(many=True)},
    tags=["My Parking Lots"]
)

# Function-based View Documentation Decorators
SEARCH_PARKING_SPOTS_DOCS = extend_schema(
    summary="Advanced parking spot search",
    description="Search for available parking spots with location, time, and filter criteria",
    parameters=[
        LATITUDE_PARAM, LONGITUDE_PARAM, START_TIME_PARAM, END_TIME_PARAM, 
        RADIUS_PARAM, MIN_PRICE_PARAM, MAX_PRICE_PARAM, SPOT_TYPE_PARAM
    ],
    responses={
        200: SearchResultsSchema,
        400: ErrorResponseSchema
    },
    tags=["Search"]
)

DASHBOARD_STATS_DOCS = extend_schema(
    summary="Get dashboard statistics",
    description="Get comprehensive statistics for the authenticated user including bookings and earnings",
    responses={200: DashboardStatsResponseSchema},
    tags=["Dashboard"]
)
