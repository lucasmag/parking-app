from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.core.views import (
    ParkingLotViewSet,
    BookingViewSet,
    MyParkingLotsViewSet,
    search_parking_spots,
    nearby_parking_spots
)

router = DefaultRouter()
router.register(r'parking-spots', ParkingLotViewSet)
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'my-spots', MyParkingLotsViewSet, basename='my-spots')

urlpatterns = [
    path('', include(router.urls)),
    path('search/', search_parking_spots, name='search-parking-spots'),
    path('nearby/', nearby_parking_spots, name='nearby-parking-spots'),
]