from django import forms
from .models import Organization


class CreateOrg(forms.ModelForm):
    name = forms.CharField(label='Имя', max_length=128, min_length=1, required=False)
    description = forms.CharField(label='Описание организации', widget=forms.Textarea, required=False)

    class Meta:
        model = Organization
        fields = ['name', 'description']

    def clean_name(self):
        print(self.cleaned_data)
        if 'name' not in self.cleaned_data:
            raise forms.ValidationError('Введите имя организации')
        else:
            name = self.cleaned_data['name']
            if name == '':
                raise forms.ValidationError('Введите имя организации')

        return self.cleaned_data['name']
