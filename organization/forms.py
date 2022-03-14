from django import forms
from .models import Organization, Service
from staff.models import Employee


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


class AddService(forms.ModelForm):
    name = forms.CharField(label='Наименование', min_length=1, max_length=64, required=False)
    description = forms.CharField(label='Описание', widget=forms.Textarea, required=False)

    time = forms.IntegerField(label='Требуемое время в минутах', min_value=0, initial=15, required=False)
    price = forms.DecimalField(label='Цена в рублях', initial=0, required=False)

    employees = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        queryset=None
    )

    class Meta:
        model = Service
        fields = ['name', 'description', 'time', 'price']

    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('organization')
        super(AddService, self).__init__(*args, **kwargs)
        self.fields['employees'].queryset = Employee.objects.filter(organization=self.organization)

    def clean_name(self):
        if 'name' not in self.cleaned_data:
            raise forms.ValidationError('Введите наименование')
        else:
            name = self.cleaned_data['name']
            if name == '':
                raise forms.ValidationError('Введите наименование')

        return self.cleaned_data['name']

    def clean_time(self):
        if 'time' not in self.cleaned_data:
            raise forms.ValidationError('Введите время')
        else:
            time = self.cleaned_data['time']
            if time is None:
                raise forms.ValidationError('Введите время')

        return self.cleaned_data['time']

    def clean_price(self):
        if 'price' not in self.cleaned_data:
            raise forms.ValidationError('Введите цену')
        else:
            price = self.cleaned_data['price']
            if price is None:
                raise forms.ValidationError('Введите цену')

        return self.cleaned_data['price']