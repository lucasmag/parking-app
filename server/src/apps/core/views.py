# Updated views.py with PostGIS optimizations
from rest_framework import status, permissions, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.contrib.gis.db.models.functions import Distance as DistanceFunction
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.contrib.gis.db.models.functions import Distance as DistanceFunction
from datetime import datetime, timedelta
import django_filters
from apps import docs

from apps.core.models import ParkingLot, Booking
from apps.core.serializers import (
    ParkingLotListSerializer, ParkingLotDetailSerializer, CreateParkingLotSerializer,
    BookingSerializer, CreateBookingSerializer
)

class ParkingLotFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price_per_hour", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price_per_hour", lookup_expr='lte')
    spot_type = django_filters.CharFilter(field_name="spot_type")
    availability = django_filters.CharFilter(field_name="availability")

    class Meta:
        model = ParkingLot
        fields = ['min_price', 'max_price', 'spot_type', 'availability']
        fields = ['min_price', 'max_price', 'spot_type', 'availability']

@docs.PARKING_LOT_VIEWSET_DOCS
class ParkingLotViewSet(ModelViewSet):
    queryset = ParkingLot.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ParkingLotFilter
    search_fields = ['title', 'address', 'description']
    ordering_fields = ['price_per_hour', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ParkingLotListSerializer
        elif self.action == 'create':
            return CreateParkingLotSerializer
        return ParkingLotDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # PostGIS-optimized location filtering
        # PostGIS-optimized location filtering
        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')
        radius = self.request.query_params.get('radius', 10)

        if lat and lng:
            user_location = Point(float(lng), float(lat), srid=4326)
            radius_m = Distance(km=float(radius))
            
            # Use PostGIS dwithin for efficient spatial filtering
            queryset = queryset.filter(
                location__dwithin=(user_location, radius_m)
            ).annotate(
                distance=DistanceFunction('location', user_location)
            ).order_by('distance')
            user_location = Point(float(lng), float(lat), srid=4326)
            radius_m = Distance(km=float(radius))
            
            # Use PostGIS dwithin for efficient spatial filtering
            queryset = queryset.filter(
                location__dwithin=(user_location, radius_m)
            ).annotate(
                distance=DistanceFunction('location', user_location)
            ).order_by('distance')

        return queryset

# Keep BookingViewSet and MyParkingLotsViewSet as they were...
# Keep BookingViewSet and MyParkingLotsViewSet as they were...
class BookingViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'spot']
    ordering = ['-created_at']

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateBookingSerializer
        return BookingSerializer

    @action(detail=True, methods=['post'])
    def extend_session(self, request, pk=None):
        """Extend an active booking session"""
        booking = self.get_object()
        
        if booking.status != 'active':
            return Response({'error': 'Can only extend active sessions'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        additional_hours = request.data.get('hours', 1)
        additional_cost = additional_hours * booking.spot.price_per_hour
        
        # Check for conflicts
        new_end_time = booking.end_time + timedelta(hours=additional_hours)
        conflicts = Booking.objects.filter(
            spot=booking.spot,
            status__in=['confirmed', 'active'],
            start_time__lt=new_end_time,
            end_time__gt=booking.end_time
        ).exclude(id=booking.id).exists()
        
        if conflicts:
            return Response({'error': 'Cannot extend due to conflicting bookings'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        booking.end_time = new_end_time
        booking.duration_hours += additional_hours
        booking.total_price += additional_cost
        booking.save()
        
        return Response({
            'message': 'Session extended successfully',
            'new_end_time': booking.end_time,
            'additional_cost': additional_cost,
            'total_price': booking.total_price
        })

    @action(detail=True, methods=['post'])
    def cancel_booking(self, request, pk=None):
        """Cancel a pending or confirmed booking"""
        booking = self.get_object()
        
        if booking.status not in ['pending', 'confirmed']:
            return Response({'error': 'Cannot cancel this booking'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        booking.status = 'cancelled'
        booking.save()
        
        return Response({'message': 'Booking cancelled successfully'})

class MyParkingLotsViewSet(ReadOnlyModelViewSet):
    """ViewSet for parking lots owned by the current user"""
    serializer_class = ParkingLotDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ParkingLot.objects.filter(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def bookings(self, request, pk=None):
        """Get bookings for a specific owned parking lot"""
        spot = self.get_object()
        bookings = Booking.objects.filter(spot=spot).order_by('-created_at')
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_parking_spots(request):
    """Advanced search with PostGIS optimization"""
    """Advanced search with PostGIS optimization"""
    lat = request.query_params.get('lat')
    lng = request.query_params.get('lng')
    start_time = request.query_params.get('start_time')
    end_time = request.query_params.get('end_time')
    radius = float(request.query_params.get('radius', 10))
    
    if not all([lat, lng, start_time, end_time]):
        return Response({'error': 'lat, lng, start_time, and end_time are required'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    user_location = Point(float(lng), float(lat), srid=4326)
    radius_m = Distance(km=radius)
    user_location = Point(float(lng), float(lat), srid=4326)
    radius_m = Distance(km=radius)
    start_time = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
    end_time = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
    
    # Get unavailable spots for the time period
    # Get unavailable spots for the time period
    unavailable_spots = Booking.objects.filter(
        status__in=['confirmed', 'active'],
        start_time__lt=end_time,
        end_time__gt=start_time
    ).values_list('spot_id', flat=True)
    
    # PostGIS optimized query
    queryset = ParkingLot.objects.filter(
        is_active=True,
        location__dwithin=(user_location, radius_m)
    ).exclude(
        id__in=unavailable_spots
    ).annotate(
        distance=DistanceFunction('location', user_location)
    ).order_by('distance')
    # PostGIS optimized query
    queryset = ParkingLot.objects.filter(
        is_active=True,
        location__dwithin=(user_location, radius_m)
    ).exclude(
        id__in=unavailable_spots
    ).annotate(
        distance=DistanceFunction('location', user_location)
    ).order_by('distance')
    
    # Serialize results
    results = []
    for spot in queryset:
        serializer = ParkingLotListSerializer(spot, context={'request': request})
        data = serializer.data
        data['distance'] = round(spot.distance.km, 2)
        results.append(data)
    
    return Response({
        'count': len(results),
        'results': results
    })

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def nearby_parking_spots(request):
    lat = request.query_params.get('latitude')
    lng = request.query_params.get('longitude')
    radius = float(request.query_params.get('radius', 5))
    limit = int(request.query_params.get('limit', 10))
    
    if not lat or not lng:
        return Response({'error': 'lat and lng parameters are required'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    user_location = Point(float(lng), float(lat), srid=4326)
    radius_m = Distance(km=radius)
    
    # PostGIS optimized query with spatial indexing
    queryset = ParkingLot.objects.filter(
        is_active=True,
        available_spots__gt=0,
        location__distance_lte=(user_location, radius_m)
    ).annotate(
        distance=DistanceFunction('location', user_location)
    ).order_by('distance')[:limit]
    
    # Serialize results
    results = []
    now = datetime.now()
    
    for spot in queryset:
        # Check current availability
        current_bookings = Booking.objects.filter(
            spot=spot,
            status__in=['confirmed', 'active'],
            start_time__lte=now,
            end_time__gte=now
        ).count()
        
        available_now = max(0, spot.available_spots - current_bookings)
        
        data = {
            'id': spot.id,
            'title': spot.title,
            'address': spot.address,
            'latitude': float(spot.latitude) if spot.latitude else spot.location.y,
            'longitude': float(spot.longitude) if spot.longitude else spot.location.x,
            'spot_type': spot.spot_type,
            'price_per_hour': float(spot.price_per_hour),
            'available_spots': available_now,
            'total_spots': spot.available_spots,
            'distance': round(spot.distance.km, 2),
            'features': spot.features or [],
            'availability': spot.availability,
        }
        results.append(data)
    
    return Response({"spots": results})

# Advanced PostGIS queries for future features
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def parking_spots_in_area(request):
    """Find parking spots within a polygon area (e.g., neighborhood)"""
    # This would be used for features like "All parking in downtown area"
    pass

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def parking_route_optimization(request):
    """Find parking spots along a route (future feature)"""
    # This could integrate with routing APIs to find spots along planned routes
    pass