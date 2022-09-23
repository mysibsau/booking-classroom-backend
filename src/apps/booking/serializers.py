from rest_framework import serializers

from .models.room import Room, RoomPhoto
from .models.booking import Booking
from .models.booking_date_time import BookingDateTime
from .models.equipment_in_room import EquipmentInRoom
from .models.carousel import Carousel, CarouselPhoto


class CarouselPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarouselPhoto
        fields = ['photo', 'address', 'event']


class CarouselSerializer(serializers.ModelSerializer):
    carousel_photo = CarouselPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Carousel
        fields = ['spec_text', 'carousel_photo', ]


class BookingRoomSerializer(serializers.ModelSerializer):
    admin = serializers.SlugRelatedField(many=False, read_only=True, slug_field='full_name')

    class Meta:
        model = Room
        fields = ["address", 'admin_contact_info', 'admin', ]


class EquipmentInRoomSerializer(serializers.ModelSerializer):
    equipment = serializers.ReadOnlyField(source='equipment.name')
    description = serializers.ReadOnlyField(source='equipment.description')

    class Meta:
        model = EquipmentInRoom
        fields = ['equipment', 'description', 'count']


class RoomPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomPhoto
        fields = ["photo", ]


class BookingDateTimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookingDateTime
        fields = ['date', 'start_time', 'end_time']


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    booking_date_time = BookingDateTimeSerializer(many=True)

    class Meta:
        model = Booking
        fields = "__all__"

    def create(self, validated_data: dict):
        booking_dates = validated_data.pop("booking_date_time", None)
        booking = Booking.objects.create(**validated_data)
        for dates in booking_dates:
            BookingDateTime.objects.create(booking=booking, **dates)

        return booking


class AcceptedBookingDateTimeSerializer(serializers.ModelSerializer):
    booking_date_time = BookingDateTimeSerializer(many=True)

    class Meta:
        model = Booking
        fields = ['booking_date_time']


class RoomSerializer(serializers.ModelSerializer):
    admin = serializers.SlugRelatedField(many=False, read_only=True, slug_field='full_name')
    equipment = EquipmentInRoomSerializer(source='equipmentinroom_set', many=True)
    room_photo = RoomPhotoSerializer(many=True, read_only=True)
    bookings_in_room = serializers.SerializerMethodField('get_bookings')

    def get_bookings(self, room):
        queryset = Booking.objects.all().filter(status=2, room_id=room.id)
        serializer = AcceptedBookingDateTimeSerializer(instance=queryset, many=True, read_only=True)

        return serializer.data

    class Meta:
        model = Room
        fields = "__all__"


class MyBookingSerializer(serializers.ModelSerializer):
    room = BookingRoomSerializer()

    class Meta:
        model = Booking
        fields = "__all__"
