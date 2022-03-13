from django import forms
from .models import Employee


class EditEmployee(forms.ModelForm):
    bio = forms.CharField(label='Описание для клиентов', widget=forms.Textarea, required=False)

    class Meta:
        model = Employee
        fields = ['bio']

