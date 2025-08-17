from django.contrib import admin
from apps.core.models import ParkingLot, Booking

@admin.register(ParkingLot)
class ParkingLotAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'address', 'spot_type', 'price_per_hour', 'is_active', 'created_at')
    list_filter = ('spot_type', 'availability', 'is_active', 'created_at')
    search_fields = ('title', 'address', 'owner__email')
    readonly_fields = ('id', 'created_at', 'updated_at')

# @admin.register(ParkingLotImage)
# class ParkingLotImageAdmin(admin.ModelAdmin):
#     list_display = ('spot', 'is_primary', 'created_at')
#     list_filter = ('is_primary', 'created_at')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'spot', 'start_time', 'end_time', 
                   'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at', 'start_time')
    search_fields = ('booking_id', 'user__email', 'spot__title')
    readonly_fields = ('id', 'booking_id', 'created_at', 'updated_at')

# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ('user', 'spot', 'rating', 'booking', 'created_at')
#     list_filter = ('rating', 'created_at')
#     search_fields = ('user__email', 'spot__title')

# @admin.register(FavoriteSpot)
# class FavoriteSpotAdmin(admin.ModelAdmin):
#     list_display = ('user', 'spot', 'created_at')
#     list_filter = ('created_at',)
#     search_fields = ('user__email', 'spot__title')

# @admin.register(Notification)
# class NotificationAdmin(admin.ModelAdmin):
#     list_display = ('user', 'type', 'title', 'is_read', 'created_at')
#     list_filter = ('type', 'is_read', 'created_at')
#     search_fields = ('user__email', 'title', 'message')