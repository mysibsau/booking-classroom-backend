from rest_framework import serializers, exceptions

from .models.room import Room, RoomPhoto
from .models.booking import Booking
from .models.booking_date_time import BookingDateTime
from .models.equipment_in_room import EquipmentInRoom
from .models.carousel import Carousel, CarouselPhoto
from .models.static_date_time import StaticDateTime


class CarouselPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarouselPhoto
        fields = ['photo', 'address', 'event']


class CarouselSerializer(serializers.ModelSerializer):
    carousel_photo = CarouselPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Carousel
        fields = ['title', 'spec_text', 'carousel_photo', ]


class BookingRoomSerializer(serializers.ModelSerializer):
    admin = serializers.SlugRelatedField(many=False, read_only=True, slug_field='full_name')

    class Meta:
        model = Room
        fields = ["address", 'admin_contact_info', 'admin', ]


class EquipmentInRoomSerializer(serializers.ModelSerializer):
    equipment = serializers.ReadOnlyField(source='equipment.name')
    description = serializers.ReadOnlyField(source='equipment.description')
    is_spec_equip = serializers.ReadOnlyField(source='equipment.is_spec_equip')

    class Meta:
        model = EquipmentInRoom
        fields = ['equipment', 'is_spec_equip', 'description', 'count', ]


class RoomPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomPhoto
        fields = ["photo", ]


class BookingDateTimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookingDateTime
        fields = ['date_start', 'date_end', 'start_time', 'end_time']


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    booking_date_time = BookingDateTimeSerializer(many=True)

    class Meta:
        model = Booking
        fields = "__all__"

    def validate(self, attrs):
        date_time = attrs['booking_date_time']
        if date_time[0]['date_start'] > date_time[0]['date_end']:
            raise exceptions.ValidationError
        if date_time[0]['start_time'] is not None and date_time[0]['end_time'] is not None:
            if date_time[0]['start_time'] > date_time[0]['end_time']:
                raise exceptions.ValidationError
            return attrs
        if date_time[0]['start_time'] is not None and date_time[0]['end_time'] is None:
            raise exceptions.ValidationError
        if date_time[0]['start_time'] is None and date_time[0]['end_time'] is not None:
            raise exceptions.ValidationError

        return attrs

    def create(self, validated_data: dict):
        booking_dates = validated_data.pop("booking_date_time", None)
        booking = Booking.objects.create(**validated_data)
        for dates in booking_dates:
            BookingDateTime.objects.create(booking=booking, **dates)

        return booking


class RoomSerializer(serializers.ModelSerializer):
    admin = serializers.SlugRelatedField(many=False, read_only=True, slug_field='full_name')
    equipment = EquipmentInRoomSerializer(source='equipmentinroom_set', many=True)
    room_photo = RoomPhotoSerializer(many=True, read_only=True)
    bookings_in_room = serializers.SerializerMethodField('get_bookings')

    def get_bookings(self, room):
        queryset = Booking.objects.all().filter(status=2, room_id=room.id)
        queryset = BookingDateTime.objects.all().filter(booking_id__in=queryset)
        date_time_queryset = StaticDateTime.objects.all().filter(room_id=room.id)
        booking_date_time_serializer = BookingDateTimeSerializer(instance=queryset, many=True, read_only=True)
        static_date_time_serializer = BookingDateTimeSerializer(instance=date_time_queryset, many=True, read_only=True)

        return booking_date_time_serializer.data + static_date_time_serializer.data

    class Meta:
        model = Room
        fields = "__all__"


class MyBookingSerializer(serializers.ModelSerializer):
    room = BookingRoomSerializer()
    booking_date_time = BookingDateTimeSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = "__all__"
