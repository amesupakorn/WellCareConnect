import os
import django
import sys
from pathlib import Path

# Add project to path
sys.path.append('/Users/supakornthongaerd/Documents/Project/DevTool/WellCareConnect/wellcare')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wellcare.settings')
django.setup()

from django.db import connection

def check_tables():
    with connection.cursor() as cursor:
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = cursor.fetchall()
        print("Tables in database:")
        for table in tables:
            print(f"- {table[0]}")

if __name__ == "__main__":
    check_tables()
