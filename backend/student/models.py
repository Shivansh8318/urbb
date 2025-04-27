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
    gender = models.CharField(max_length=10, choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Other')), null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name or self.identity_value} ({self.get_user_type_display()})"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    grade = models.CharField(max_length=20, null=True, blank=True)
    school = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f"Student: {self.user.name or self.user.identity_value}"