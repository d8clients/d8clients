from django import forms
from .models import Organization


class CreateOrg(forms.ModelForm):
    name = forms.CharField(label='Имя', max_length=128, min_length=1)
    description = forms.CharField(label='Описание организации', widget=forms.Textarea)

    class Meta:
        model = Organization
        fields = ['name', 'description']