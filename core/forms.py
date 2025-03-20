from django import forms
from .models import MaintenanceLog

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = MaintenanceLog
        fields = ['equipment', 'maintenance_date', 'description', 'performed_by', 'cost']