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

    def to_internal_value(self, data):
        """
        Custom data transformation before validation.
        Maps fields and converts Thai formats.
        """
        # Create a mutable copy of the data
        mutable_data = data.copy() if hasattr(data, 'copy') else dict(data)

        # Map 'booker' from 'first_name'/'last_name' or 'firstname'/'lastname'
        fn = mutable_data.get('first_name') or mutable_data.get('firstname')
        ln = mutable_data.get('last_name') or mutable_data.get('lastname')
        if fn and ln:
            mutable_data['booker'] = f"{fn} {ln}"

        # Map 'date' to 'date_reserve' if provided
        if 'date' in mutable_data:
            mutable_data['date_reserve'] = mutable_data['date']

        # Map 'time_start' or 'time' to 'time_reserve' if provided
        tm = mutable_data.get('time_start') or mutable_data.get('time')
        if tm:
            mutable_data['time_reserve'] = tm

        # Map 'location_id' to 'location' if provided
        if 'location_id' in mutable_data:
            mutable_data['location'] = mutable_data['location_id']

        # Convert Thai date (BE) to Gregorian (CE)
        if 'date_reserve' in mutable_data and mutable_data['date_reserve']:
            try:
                date_val = mutable_data['date_reserve']
                if '/' in date_val:
                    day, month, buddhist_year = map(int, date_val.split('/'))
                    gregorian_year = buddhist_year - 543
                    mutable_data['date_reserve'] = f'{gregorian_year}-{month:02d}-{day:02d}'
            except (ValueError, AttributeError):
                pass # Validation will handle incorrect formats

        # Clean time (remove 'น.')
        if 'time_reserve' in mutable_data and mutable_data['time_reserve']:
            try:
                time_val = mutable_data['time_reserve']
                mutable_data['time_reserve'] = time_val.replace('น.', '').strip()
            except AttributeError:
                pass

        return super().to_internal_value(mutable_data)
