from django.db import models
from django.contrib.auth.models import User


class Disease(models.Model):
    disease_name = models.CharField(max_length=255, unique=True)  # ชื่อของโรค
    description = models.TextField()  # คำอธิบายเกี่ยวกับโรค
    symptoms = models.TextField()  # อาการของโรค
    treatment = models.TextField()  # วิธีการรักษาเบื้องต้น
    medication = models.TextField()  # ยารักษาโรค

    def __str__(self):
        return self.disease_name

class Location(models.Model):
    BOOKING_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    ]

    name = models.CharField(max_length=100)
    opening = models.TimeField()
    closing = models.TimeField()
    status = models.CharField(max_length=20)
    booking_status = models.CharField(max_length=20, choices=BOOKING_CHOICES, default='available')
    staff = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.name
    
class Booking(models.Model):
    booker = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    symptoms = models.CharField(max_length=255)
    date_reserve = models.DateField()
    time_reserve = models.TimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)