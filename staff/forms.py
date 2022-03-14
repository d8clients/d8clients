from django import forms
from .models import Employee, WorkDay
from organization.models import Service


class EditEmployee(forms.ModelForm):
    bio = forms.CharField(label='Описание для клиентов', widget=forms.Textarea, required=False)

    services = forms.ModelMultipleChoiceField(
        label="Услуги",
        required=False,
        widget=forms.CheckboxSelectMultiple,
        queryset=None
    )

    class Meta:
        model = Employee
        fields = ['bio', 'services']

    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('organization')
        super(EditEmployee, self).__init__(*args, **kwargs)
        self.fields['services'].queryset = Service.objects.filter(organization=self.organization)


class WorkDayForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(format='%m/%d/%y'))
    start = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    end = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))

    class Meta:
        model = WorkDay
        fields = '__all__'
