from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TimeSlotViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'timeslots', TimeSlotViewSet, basename='timeslot')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
] 