from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Room,Booking
from .serializers import RoomSerializer,BookingSerializer

from rest_framework.decorators import action
from rest_framework.response import Response


class RoomViewSet(ModelViewSet):
    queryset=Room.objects.all()
    serializer_class=RoomSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]   

    @action(detail=True, methods=["get"])
    def bookings(self, request, pk=None):
        room = self.get_object()
        bookings = room.bookings.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    

    @action(detail=False, methods=["get"])
    def free(self, request):
        start_time = request.GET.get("start_time")
        end_time = request.GET.get("end_time")

        if not start_time or not end_time:
            return Response({"error": "start_time and end_time required"})

        if end_time <= start_time:
            return Response({"error": "end_time must be after start_time"})
        
        
        blocking_bookings = Booking.objects.filter(
            start_time__lt=end_time,
            end_time__gt=start_time
        ).values_list("room_id", flat=True)

        free_rooms = Room.objects.exclude(id__in=blocking_bookings)

        serializer = RoomSerializer(free_rooms, many=True)
        return Response(serializer.data)

class BookingViewSet(ModelViewSet):
    queryset=Booking.objects.all()
    serializer_class=BookingSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]
    
    




