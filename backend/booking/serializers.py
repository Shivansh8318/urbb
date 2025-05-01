from rest_framework import serializers
from .models import TimeSlot, Booking
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TimeSlotSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    
    class Meta:
        model = TimeSlot
        fields = ['id', 'teacher', 'start_time', 'end_time', 'is_booked', 'created_at']
        read_only_fields = ['is_booked']

class BookingSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    time_slot = TimeSlotSerializer(read_only=True)
    time_slot_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'student', 'time_slot', 'time_slot_id', 'status', 'created_at']
        read_only_fields = ['student', 'status'] 