from rest_framework import status, permissions, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, F, Value
from django.db.models.functions import Sqrt, Power
from geopy.distance import geodesic
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
    min_rating = django_filters.NumberFilter(field_name="rating", lookup_expr='gte')

    class Meta:
        model = ParkingLot
        fields = ['min_price', 'max_price', 'spot_type', 'availability', 'min_rating']

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
        
        # Location-based filtering
        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')
        radius = self.request.query_params.get('radius', 10)

        if lat and lng:
            lat, lng = float(lat), float(lng)
            queryset = queryset.annotate(
                distance=Sqrt(
                    Power((F('latitude') - lat) * 111.32, 2) +
                    Power((F('longitude') - lng) * 111.32 * 0.8, 2)
                )
            ).filter(distance__lte=float(radius)).order_by('distance')

        return queryset

    @docs.PARKING_LOT_AVAILABILITY_DOCS
    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """Get parking lot availability for a specific date"""
        spot = self.get_object()
        date = request.query_params.get('date', datetime.now().date())
        
        bookings = Booking.objects.filter(
            spot=spot,
            status__in=['confirmed', 'active'],
            start_time__date__lte=date,
            end_time__date__gte=date
        ).values('start_time', 'end_time')
        
        return Response({
            'spot_id': spot.id,
            'date': date,
            'booked_slots': list(bookings)
        })

@docs.BOOKING_VIEWSET_DOCS
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

    @docs.BOOKING_EXTEND_SESSION_DOCS
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

    @docs.BOOKING_CANCEL_DOCS
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


@docs.MY_PARKING_LOTS_VIEWSET_DOCS
class MyParkingLotsViewSet(ReadOnlyModelViewSet):
    """ViewSet for parking lots owned by the current user"""
    serializer_class = ParkingLotDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ParkingLot.objects.filter(owner=self.request.user)

    @docs.MY_PARKING_LOT_BOOKINGS_DOCS
    @action(detail=True, methods=['get'])
    def bookings(self, request, pk=None):
        """Get bookings for a specific owned parking lot"""
        spot = self.get_object()
        bookings = Booking.objects.filter(spot=spot).order_by('-created_at')
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

# class ReviewViewSet(ModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     filter_backends = [filters.OrderingFilter]
#     ordering = ['-created_at']

#     def get_queryset(self):
#         spot_id = self.request.query_params.get('spot_id')
#         if spot_id:
#             return Review.objects.filter(spot_id=spot_id)
#         return Review.objects.filter(user=self.request.user)

#     def get_serializer_class(self):
#         if self.action == 'create':
#             return CreateReviewSerializer
#         return ReviewSerializer

# class FavoriteSpotViewSet(ReadOnlyModelViewSet):
#     serializer_class = FavoriteSpotSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return FavoriteSpot.objects.filter(user=self.request.user)

# class NotificationViewSet(ModelViewSet):
#     serializer_class = NotificationSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     filter_backends = [filters.OrderingFilter]
#     ordering = ['-created_at']

#     def get_queryset(self):
#         return Notification.objects.filter(user=self.request.user)

    # @action(detail=False, methods=['post'])
    # def mark_all_read(self, request):
    #     self.get_queryset().update(is_read=True)
    #     return Response({'message': 'All notifications marked as read'})

    # @action(detail=True, methods=['post'])
    # def mark_read(self, request, pk=None):
    #     notification = self.get_object()
    #     notification.is_read = True
    #     notification.save()
    #     return Response({'message': 'Notification marked as read'})

@docs.SEARCH_PARKING_SPOTS_DOCS
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_parking_spots(request):
    """Advanced search with location, time, and filters"""
    lat = request.query_params.get('lat')
    lng = request.query_params.get('lng')
    start_time = request.query_params.get('start_time')
    end_time = request.query_params.get('end_time')
    radius = float(request.query_params.get('radius', 10))
    
    if not all([lat, lng, start_time, end_time]):
        return Response({'error': 'lat, lng, start_time, and end_time are required'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    lat, lng = float(lat), float(lng)
    start_time = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
    end_time = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
    
    # Get available spots
    unavailable_spots = Booking.objects.filter(
        status__in=['confirmed', 'active'],
        start_time__lt=end_time,
        end_time__gt=start_time
    ).values_list('spot_id', flat=True)
    
    queryset = ParkingLot.objects.filter(is_active=True).exclude(id__in=unavailable_spots)
    
    # Filter by location
    spots_with_distance = []
    for spot in queryset:
        distance = geodesic((lat, lng), (spot.latitude, spot.longitude)).kilometers
        if distance <= radius:
            spots_with_distance.append((spot, distance))
    
    # Sort by distance
    spots_with_distance.sort(key=lambda x: x[1])
    
    # Serialize results
    results = []
    for spot, distance in spots_with_distance:
        serializer = ParkingLotListSerializer(spot, context={'request': request})
        data = serializer.data
        data['distance'] = round(distance, 2)
        results.append(data)
    
    return Response({
        'count': len(results),
        'results': results
    })

@docs.DASHBOARD_STATS_DOCS
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats(request):
    """Get dashboard statistics for the user"""
    user = request.user
    
    # User stats
    total_bookings = Booking.objects.filter(user=user).count()
    active_bookings = Booking.objects.filter(user=user, status='active').count()
    upcoming_bookings = Booking.objects.filter(
        user=user, 
        status='confirmed',
        start_time__gt=datetime.now()
    ).count()
    
    # Owner stats (if user owns spots)
    owned_spots = ParkingLot.objects.filter(owner=user).count()
    total_earnings = sum(
        booking.total_price for booking in 
        Booking.objects.filter(spot__owner=user, status='completed')
    )
    
    return Response({
        'user_stats': {
            'total_bookings': total_bookings,
            'active_bookings': active_bookings,
            'upcoming_bookings': upcoming_bookings,
            'reward_points': user.reward_points,
        },
        'owner_stats': {
            'owned_spots': owned_spots,
            'total_earnings': float(total_earnings),
        }
    })
