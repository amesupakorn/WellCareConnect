# Generated by Django 5.1.2 on 2024-10-13 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connects', '0002_location_booking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='date_now',
        ),
    ]
