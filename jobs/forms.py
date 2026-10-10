
from django import forms
from .models import job


class JobForm(forms.ModelForm):
    class Meta:
        model = job
        fields = [
            'title',
            'company_name',
            'description',
            'location',
            'salary',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'e.g. Python Developer',
            }),
            'company_name': forms.TextInput(attrs={
                'placeholder': 'Enter company name',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Describe the role and responsibilities',
                'rows': 5,
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'e.g. Chandigarh',
            }),
            'salary': forms.NumberInput(attrs={
                'placeholder': 'Enter salary',
                'min': '0',
                'step': '0.01',
            }),
        }
