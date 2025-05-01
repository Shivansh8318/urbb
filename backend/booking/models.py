from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class TimeSlot(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_slots')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.teacher.username}'s slot: {self.start_time} - {self.end_time}"

class Booking(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_bookings')
    time_slot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE, related_name='booking')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled')
    ], default='PENDING')

    def __str__(self):
        return f"{self.student.username}'s booking for {self.time_slot}" 