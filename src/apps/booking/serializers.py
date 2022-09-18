from rest_framework import serializers

from .models.room import Room, RoomPhoto
from .models.equipment import Equipment
from .models.booking import Booking
from .models.booking_date_time import BookingDateTime


class EquipmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Equipment
        fields = "__all__"


class RoomPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomPhoto
        fields = ["id", "photo", ]


class BookingDateTimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookingDateTime
        fields = ['date', 'start_time', 'end_time']


class RoomSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer(many=True, read_only=True)
    room_photo = RoomPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = "__all__"


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
