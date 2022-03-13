from django import forms
from .models import Organization


class CreateOrg(forms.ModelForm):
    name = forms.CharField(label='Имя', max_length=128, min_length=1, required=False)
    description = forms.CharField(label='Описание организации', widget=forms.Textarea, required=False)

    class Meta:
        model = Organization
        fields = ['name', 'description']

    def clean_name(self):
        if 'name' not in self.cleaned_data:
            raise forms.ValidationError('Введите имя организации')
        else:
            name = self.cleaned_data['name']
            if name == '':
                raise forms.ValidationError('Введите имя организации')

        return self.cleaned_data['name']


class AddEmployee(forms.Form):
    email = forms.EmailField(required=False)

    def clean_email(self):
        if 'email' not in self.cleaned_data:
            raise forms.ValidationError('Введите e-mail')
        else:
            email = self.cleaned_data['email']
            if email == '':
                raise forms.ValidationError('Введите e-mail')

        return self.cleaned_data['email']


class AddAdmin(forms.Form):
    email = forms.EmailField(required=False)

    def clean_email(self):
        if 'email' not in self.cleaned_data:
            raise forms.ValidationError('Введите e-mail')
        else:
            email = self.cleaned_data['email']
            if email == '':
                raise forms.ValidationError('Введите e-mail')

        return self.cleaned_data['email']