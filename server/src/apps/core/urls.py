from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ParkingLotViewSet,
    BookingViewSet,
    MyParkingLotsViewSet,
    search_parking_spots,
    dashboard_stats,
)

router = DefaultRouter()
router.register(r'parking-spots', ParkingLotViewSet)
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'my-spots', MyParkingLotsViewSet, basename='my-spots')

urlpatterns = [
    path('', include(router.urls)),
    path('search/', search_parking_spots, name='search-parking-spots'),
    path('dashboard/', dashboard_stats, name='dashboard-stats'),
]