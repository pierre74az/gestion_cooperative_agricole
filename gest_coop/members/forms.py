# members/forms.py

from django import forms
from .models import Member

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'role', 'email', 'phone', 'bio', 'photo']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
