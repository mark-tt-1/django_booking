from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RoomViewSet,BookingViewSet

router = DefaultRouter()
router.register("rooms",RoomViewSet,basename="rooms")
# 127.... /rooms/
router.register("bookings", BookingViewSet, basename="bookings")
urlpatterns = [
    path("", include(router.urls)),    
]