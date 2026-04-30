import os
import django
import sys
from django.utils import timezone
from datetime import time

# Add project to path
sys.path.append('/Users/supakornthongaerd/Documents/Project/DevTool/WellCareConnect/wellcare')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wellcare.settings')
django.setup()

from django.contrib.auth.models import User
from connects.models import Location

def add_location():
    # 1. Create or get a staff user
    username = 'staff_kmitl'
    staff_user, created = User.objects.get_or_create(username=username)
    if created:
        staff_user.set_password('kmitl1234')
        staff_user.save()
        print(f"Created new staff user: {username}")
    else:
        print(f"Using existing staff user: {username}")

    # 2. Add Location
    location_name = "คลินิก kmitl"
    location, loc_created = Location.objects.get_or_create(
        name=location_name,
        defaults={
            'opening': time(8, 0),
            'closing': time(17, 0),
            'status': 'Open',
            'booking_status': 'available',
            'staff': staff_user
        }
    )

    if loc_created:
        print(f"Successfully added location: {location_name}")
    else:
        # If already exists but staff is different or needs update
        location.staff = staff_user
        location.save()
        print(f"Location {location_name} already exists. Updated staff info.")

if __name__ == "__main__":
    add_location()
