from rest_framework import serializers
from datetime import datetime
from .models import Booking, Location

class ReserveSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Booking
        fields = [
            'booker',
            'phone',
            'symptoms',
            'date_reserve',
            'time_reserve',
            'location'
        ]

    def __init__(self, *args, **kwargs):
        """
        ตรวจสอบและแปลงค่าที่ได้รับตั้งแต่ตอนเริ่มต้น
        """
        super(ReserveSerializer, self).__init__(*args, **kwargs)

        # แปลงวันที่และเวลาหากได้รับข้อมูล
        if 'data' in kwargs:
            # แปลงวันที่เป็นคริสต์ศักราช
            if 'date_reserve' in kwargs['data']:
                kwargs['data']['date_reserve'] = self.convert_thai_date(kwargs['data']['date_reserve'])

            # แปลงเวลาลบ 'น.'
            if 'time_reserve' in kwargs['data']:
                kwargs['data']['time_reserve'] = self.clean_time(kwargs['data']['time_reserve'])

    def convert_thai_date(self, value):
        """
        แปลงวันที่จากพุทธศักราชเป็นคริสต์ศักราช
        """
        try:
            day, month, buddhist_year = map(int, value.split('/'))
            gregorian_year = buddhist_year - 543
            gregorian_date = f'{gregorian_year}-{month:02d}-{day:02d}'
            return gregorian_date  # ส่งกลับรูปแบบ YYYY-MM-DD
        except ValueError:
            raise serializers.ValidationError("รูปแบบวันที่ไม่ถูกต้อง, ควรใช้รูปแบบ dd/mm/yyyy")

    def clean_time(self, value):
        """
        ลบอักษร 'น.' และแปลงเป็นเวลาในรูปแบบ HH:MM
        """
        try:
            clean_time = value.replace('น.', '').strip()
            return clean_time
        except ValueError:
            raise serializers.ValidationError("รูปแบบเวลาไม่ถูกต้อง, ควรใช้ HH:MM")
