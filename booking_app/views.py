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
    

class BookingViewSet(ModelViewSet):
    queryset=Booking.objects.all()
    serializer_class=BookingSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]
    
    




