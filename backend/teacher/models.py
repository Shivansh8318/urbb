from django.db import models

class User(models.Model):
    USER_TYPES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    
    user_id = models.CharField(max_length=255, unique=True)
    identity_type = models.CharField(max_length=50)
    identity_value = models.CharField(max_length=255)
    name = models.CharField(max_length=255, null=True, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name or self.identity_value} ({self.get_user_type_display()})"

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    subject = models.CharField(max_length=100, null=True, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"Teacher: {self.user.name or self.user.identity_value}"