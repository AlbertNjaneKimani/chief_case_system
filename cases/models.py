from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    ROLE_CHOICES = (
        ('complainant', 'Complainant'),
        ('chief', 'Chief'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    groups = models.ManyToManyField(Group, related_name='cases_users')
    user_permissions = models.ManyToManyField(Permission, related_name='cases_users_permissions')
class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(null=True, blank=True)
    national_id = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    location = models.CharField(max_length=255)
    sublocation = models.CharField(max_length=255)
    county = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username}'s profile"
class Case(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('solved', 'Solved'),
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    complainant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cases')
    casecategory = models.CharField(max_length=100) 

    def __str__(self):
        return self.title

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('aactive', 'Active'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    )
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    appointment_status=models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    location = models.CharField(max_length=255)
    chief = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    complainant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complainant_appointments')

    def __str__(self):
        return f"{self.case.title} - {self.date} {self.time}"
# Create your models here.
