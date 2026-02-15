from rest_framework import serializers
from .models import Room, Booking


from django.db import transaction
from django.utils import timezone
import logging


logger = logging.getLogger(__name__)

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

        start_time = data["start_time"]
        end_time = data["end_time"]
        user_name = data["user_name"]

        if end_time <= start_time:
            raise serializers.ValidationError(
                "Время выезда должен быть позже времени заезда"
            )
        
    
        now = timezone.now()

        active_bookings_count = Booking.objects.filter(
            user_name=user_name,
            end_time__gt=now
        ).count()

        if active_bookings_count >= 3:
            raise serializers.ValidationError(
                "У пользователя не может быть более 3 активных броней"
            )
        
        time_dif = (start_time - now).total_seconds()

        if 0 <= time_dif < 600:
            logger.warning(
                f"Booking created less than 10 minutes before start. "
                f"User: {user_name}"
            )
        return data
    

    def create(self, validated_data):
        with transaction.atomic():
            booking = Booking.objects.create(**validated_data)
        return booking