from rest_framework import serializers
from .models import ParkingLot, Booking
from django.contrib.auth import get_user_model

User = get_user_model()

# class ParkingLotImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ParkingLotImage
#         fields = ['id', 'image', 'is_primary', 'created_at']

class ParkingLotListSerializer(serializers.ModelSerializer):
    # images = ParkingLotImageSerializer(many=True, read_only=True)
    distance = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)
    # is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = ParkingLot
        fields = ['id', 'title', 'address', 'latitude', 'longitude', 'spot_type',
                 'price_per_hour', 'distance']

    # def get_is_favorite(self, obj):
    #     request = self.context.get('request')
    #     if request and request.user.is_authenticated:
    #         return FavoriteSpot.objects.filter(user=request.user, spot=obj).exists()
    #     return False

class ParkingLotDetailSerializer(serializers.ModelSerializer):
    # images = ParkingLotImageSerializer(many=True, read_only=True)
    owner_name = serializers.CharField(source='owner.full_name', read_only=True)
    # is_favorite = serializers.SerializerMethodField()
    upcoming_bookings = serializers.SerializerMethodField()

    class Meta:
        model = ParkingLot
        fields = ['id', 'title', 'description', 'address', 'latitude', 'longitude',
                 'spot_type', 'price_per_hour', 'availability',
                 'features', 'instructions', 'owner_name',
                 'upcoming_bookings', 'created_at']

    # def get_is_favorite(self, obj):
    #     request = self.context.get('request')
    #     if request and request.user.is_authenticated:
    #         return FavoriteSpot.objects.filter(user=request.user, spot=obj).exists()
    #     return False

    def get_upcoming_bookings(self, obj):
        from datetime import datetime, timedelta
        now = datetime.now()
        upcoming = Booking.objects.filter(
            spot=obj,
            status__in=['confirmed', 'active'],
            start_time__gte=now,
            start_time__lte=now + timedelta(days=7)
        ).values('start_time', 'end_time')
        return list(upcoming)

class CreateParkingLotSerializer(serializers.ModelSerializer):
    # images = serializers.ListField(
    #     child=serializers.ImageField(),
    #     write_only=True,
    #     required=False
    # )

    class Meta:
        model = ParkingLot
        fields = ['title', 'description', 'address', 'latitude', 'longitude',
                 'spot_type', 'price_per_hour', 'availability', 'features',
                 'instructions',]

    def create(self, validated_data):
        # images_data = validated_data.pop('images', [])
        spot = ParkingLot.objects.create(owner=self.context['request'].user, **validated_data)
        
        # for i, image_data in enumerate(images_data):
        #     ParkingLotImage.objects.create(
        #         spot=spot,
        #         image=image_data,
        #         is_primary=(i == 0)
        #     )
        # return spot

class BookingSerializer(serializers.ModelSerializer):
    spot_title = serializers.CharField(source='spot.title', read_only=True)
    spot_address = serializers.CharField(source='spot.address', read_only=True)
    spot_image = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ['id', 'booking_id', 'spot', 'spot_title', 'spot_address', 'spot_image',
                 'start_time', 'end_time', 'duration_hours', 'total_price', 'status',
                 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'booking_id', 'created_at', 'updated_at']

    def get_spot_image(self, obj):
        primary_image = obj.spot.images.filter(is_primary=True).first()
        if primary_image:
            return primary_image.image.url
        return None

class CreateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['spot', 'start_time', 'end_time', 'duration_hours', 'notes']

    def validate(self, attrs):
        spot = attrs.get('spot')
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')

        # Check for overlapping bookings
        overlapping = Booking.objects.filter(
            spot=spot,
            status__in=['confirmed', 'active'],
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists()

        if overlapping:
            raise serializers.ValidationError("This time slot is already booked.")

        # Calculate total price
        duration_hours = attrs.get('duration_hours')
        attrs['total_price'] = duration_hours * spot.price_per_hour

        return attrs

    def create(self, validated_data):
        return Booking.objects.create(user=self.context['request'].user, **validated_data)

# class ReviewSerializer(serializers.ModelSerializer):
#     user_name = serializers.CharField(source='user.full_name', read_only=True)

#     class Meta:
#         model = Review
#         fields = ['id', 'rating', 'comment', 'user_name', 'created_at']
#         read_only_fields = ['id', 'user_name', 'created_at']

# class CreateReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = ['booking', 'rating', 'comment']

#     def create(self, validated_data):
#         user = self.context['request'].user
#         booking = validated_data['booking']
#         return Review.objects.create(
#             user=user,
#             spot=booking.spot,
#             **validated_data
#         )

# class FavoriteSpotSerializer(serializers.ModelSerializer):
#     spot = ParkingLotListSerializer(read_only=True)

#     class Meta:
#         model = FavoriteSpot
#         fields = ['id', 'spot', 'created_at']

# class NotificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Notification
#         fields = ['id', 'type', 'title', 'message', 'is_read', 'booking', 'spot', 'created_at']
#         read_only_fields = ['id', 'created_at']