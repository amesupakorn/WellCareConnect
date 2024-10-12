from django import forms 
from .models import Form as F
from django.utils import timezone
from django.core.exceptions import ValidationError
class ReserveForm(forms.ModelForm):
    class Meta:
        model = F
        fields = [
            'first_name',
            'last_name',
            'phone',
            'symptoms',
            'date_reserve',
            'time_reserve',
            'location'
        ]
        widgets = {
            'date_reserve': forms.DateInput(attrs={'type': 'date'})
        }

    def clean_date_reserve(self):
        date_reserve = self.cleaned_data.get('date_reserve')
        if date_reserve < timezone.now().date():
            raise ValidationError("You cannot reserve a date in the past.")
        return date_reserve
