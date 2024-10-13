from django.db import models


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

    def __str__(self):
        return self.name
    
class Booking(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()
    phone = models.CharField()
    symptoms = models.CharField()
    date_now = models.DateField(auto_now=False, auto_now_add=True)
    date_reserve = models.DateField()
    time_reserve = models.TimeField()
    location = models.CharField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)