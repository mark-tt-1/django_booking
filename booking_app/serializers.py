from rest_framework import serializers
from .models import Room, Booking


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            "id",
            "name",
            "capacity",
            "has_projector",
        ]


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = [
            "id",
            "room",
            "user_name",
            "start_time",
            "end_time",
            "created_at",
        ]
        read_only_fields = ["created_at"]

    def validate(self, data):
        if data["end_time"] <= data["start_time"]:
            raise serializers.ValidationError(
                "Время выезда должен быть позже времени заезда"
            )
        return data