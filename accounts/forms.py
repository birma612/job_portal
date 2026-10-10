
from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'phone_number',
            'education',
            'skills',
            'professional_summary',
            'resume',
        ]

        widgets = {
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Enter your phone number',
            }),
            'education': forms.TextInput(attrs={
                'placeholder': 'e.g. MSc Information Technology',
            }),
            'skills': forms.Textarea(attrs={
                'placeholder': 'e.g. Python, Django, SQL',
                'rows': 3,
            }),
            'professional_summary': forms.Textarea(attrs={
                'placeholder': 'Write a short professional introduction',
                'rows': 4,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': (
                    'w-full rounded-xl border border-white '
                    'bg-white/80 px-4 py-3 text-sm text-slate-800 '
                    'outline-none focus:border-blue-300 '
                    'focus:ring-2 focus:ring-blue-200'
                )
            })

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')

        if not resume:
            return resume

        if resume.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                'Resume file must be 5 MB or smaller.'
            )

        if not resume.name.lower().endswith('.pdf'):
            raise forms.ValidationError(
                'Please upload your resume as a PDF file.'
            )

        return resume
