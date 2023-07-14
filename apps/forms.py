from django import forms
from apps.models import *

class TicketBookingForm(forms.ModelForm):
    class Meta:
        model = BookingMaster
        fields = ['event', 'tickets']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Exclude fields you want to hide
            self.fields.pop('is_deleted')
