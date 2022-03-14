from django import forms
from .models import Employee
from organization.models import Service


class EditEmployee(forms.ModelForm):
    bio = forms.CharField(label='Описание для клиентов', widget=forms.Textarea, required=False)

    services = forms.MultipleChoiceField(
        label="Услуги",
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Employee
        fields = ['bio', 'services']

    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('organization')
        super(EditEmployee, self).__init__(*args, **kwargs)
        self.fields['services'].choices = [(ser.id, ser) for ser in Service.objects.filter(organization=self.organization)]