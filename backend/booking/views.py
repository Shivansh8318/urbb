from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth.models import User
from .models import TimeSlot, Booking
from .serializers import TimeSlotSerializer, BookingSerializer
import logging

logger = logging.getLogger(__name__)

class TimeSlotViewSet(viewsets.ModelViewSet):
    serializer_class = TimeSlotSerializer

    def get_queryset(self):
        # Get the default teacher user
        default_teacher = User.objects.get(username='default_teacher')
        # Return all slots for the default teacher
        return TimeSlot.objects.filter(teacher=default_teacher).order_by('-start_time')

    def perform_create(self, serializer):
        try:
            logger.info('Creating new time slot with data: %s', serializer.validated_data)
            # Get or create a default teacher user
            default_teacher, created = User.objects.get_or_create(
                username='default_teacher',
                defaults={
                    'email': 'default_teacher@example.com',
                    'is_staff': True
                }
            )
            serializer.save(teacher=default_teacher)
            logger.info('Time slot created successfully')
        except Exception as e:
            logger.error('Error creating time slot: %s', str(e))
            raise serializers.ValidationError(f"Error creating time slot: {str(e)}")

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer

    def get_queryset(self):
        return Booking.objects.all()

    def perform_create(self, serializer):
        try:
            time_slot = TimeSlot.objects.get(id=serializer.validated_data['time_slot_id'])
            if time_slot.is_booked:
                raise serializers.ValidationError("This time slot is already booked")
            
            # Get or create a default student user
            default_student, created = User.objects.get_or_create(
                username='default_student',
                defaults={
                    'email': 'default_student@example.com'
                }
            )
            
            time_slot.is_booked = True
            time_slot.save()
            serializer.save(student=default_student, time_slot=time_slot)
        except TimeSlot.DoesNotExist:
            raise serializers.ValidationError("Time slot not found")
        except Exception as e:
            logger.error('Error creating booking: %s', str(e))
            raise serializers.ValidationError(f"Error creating booking: {str(e)}")

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        try:
            booking = self.get_object()
            if booking.status == 'CANCELLED':
                return Response({'error': 'Booking is already cancelled'}, status=status.HTTP_400_BAD_REQUEST)
            
            booking.status = 'CANCELLED'
            booking.time_slot.is_booked = False
            booking.time_slot.save()
            booking.save()
            return Response({'status': 'booking cancelled'})
        except Exception as e:
            logger.error('Error cancelling booking: %s', str(e))
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 