from rest_framework import serializers
from .models import *

class ReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'first_name',
            'last_name',
            'phone',
            'symptoms',
            'date_reserve',
            'time_reserve',
            'location'
        ]

