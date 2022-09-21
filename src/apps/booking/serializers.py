from rest_framework import serializers

from .models.room import Room, RoomPhoto
from .models.equipment import Equipment
from .models.booking import Booking
from .models.booking_date_time import BookingDateTime
from .models.equipment_in_room import EquipmentInRoom


class BookingRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ["address", ]


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


class RoomSerializer(serializers.ModelSerializer):
    equipment = EquipmentInRoomSerializer(source='equipmentinroom_set', many=True)
    room_photo = RoomPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    booking_date_time = BookingDateTimeSerializer(many=True)
    room = BookingRoomSerializer()

    class Meta:
        model = Booking
        fields = "__all__"

    def create(self, validated_data: dict):
        booking_dates = validated_data.pop("booking_date_time", None)
        booking = Booking.objects.create(**validated_data)
        for dates in booking_dates:
            BookingDateTime.objects.create(booking=booking, **dates)

        return booking
