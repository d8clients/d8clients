from django import forms
from .models import Organization, Service
#from .assign_model import Assignment
from staff.models import Employee, WorkDay
from datetime import datetime, time, date, timedelta


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


class CreateAssignmentStep1(forms.Form):

    service = forms.ModelChoiceField(
        label='Выберите услугу',
        required=False,
        widget=forms.Select(attrs={'placeholder': 'Выберите услугу'}),
        queryset=None
    )

    employee = forms.ModelChoiceField(
        label='Выберите сотрудника',
        required=False,
        widget=forms.Select(attrs={'placeholder': 'Выберите сотрудника'}),
        queryset=None
    )

    date = forms.DateField(label='', widget=forms.DateInput(attrs={'placeholder': 'Напишите дату в формате dd/mm/yyyy'}),
                           required=False)

    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('organization')
        super(CreateAssignmentStep1, self).__init__(*args, **kwargs)
        self.fields['employee'].queryset = Employee.objects.filter(organization=self.organization)
        self.fields['service'].queryset = Service.objects.filter(organization=self.organization)

    def clean(self):
        cd = self.cleaned_data
        valid_errs = []

        if 'employee' not in cd or cd['employee'] is None:
            valid_errs.append(forms.ValidationError('Выберите сотрудника'))

        if 'service' not in cd or cd['service'] is None:
            valid_errs.append(forms.ValidationError('Выберите услугу'))

        if 'date' not in cd or cd['date'] is None:
            valid_errs.append(forms.ValidationError('Выберите дату'))

        if valid_errs:
            raise forms.ValidationError(valid_errs)
            return

        if cd['date'] < date.today():
            valid_errs.append(forms.ValidationError('Вы выбрали уже прошедшую дату'))

        if not cd['employee'].services.filter(id=cd['service'].id).exists():
            valid_errs.append(forms.ValidationError(
                'Данный сотрудник не предоставляет данную услугу'))

        if not cd['employee'].workdays.filter(date=cd['date']).exists():
            valid_errs.append(forms.ValidationError(
                'Данный сотрудник не работает в этот день'))

        if valid_errs:
            raise forms.ValidationError(valid_errs)


class CreateAssignmentStep2(forms.Form):

    start = forms.ChoiceField(
        label='Выберите подходящее вам время',
        required=False,
        widget=forms.Select(attrs={'placeholder': 'Выберите подходяшее время'}),
    )

    def __init__(self, *args, **kwargs):
        self.workday = kwargs.pop('workday')
        self.service = kwargs.pop('service')
        super(CreateAssignmentStep2, self).__init__(*args, **kwargs)

        self.fields['start'].choices = []
        delta = timedelta(minutes=5)

        # list отрезков на прямой времени, когда есть запись
        ass_list = [(self.workday.start, self.workday.start)] + \
                   [(ass.start, (datetime.combine(date.today(), ass.start) + timedelta(minutes=ass.service.time)).time())
                    for ass in self.workday.employee.assignments.filter(date=self.workday.date).filter(confirmed=True).order_by('start')]

        # проходимся по всем свободным отрезкам с интервалом в 5 минут,
        # кроме [конец последней записи, конец рабочего дня]
        for ass_id in range(1, len(ass_list)):
            end0 = ass_list[ass_id][0]

            while (datetime.combine(date.today(), ass_list[ass_id - 1][1]) + delta).time() <= end0:
                self.fields['start'].choices.append(
                    [(datetime.combine(date.today(), end0) - delta).time(),
                     (datetime.combine(date.today(), end0) - delta).time()]
                )

                end0 = (datetime.combine(date.today(), end0) - delta).time()

        # проходимся отрезку [конец последней запись, конец рабочего дня]
        end0 = (datetime.combine(date.today(), ass_list[-1][1]) + delta).time()
        while end0 < self.workday.end:
            self.fields['start'].choices.append(
                [(datetime.combine(date.today(), end0) - delta).time(),
                (datetime.combine(date.today(), end0) - delta).time()]
            )
            end0 = datetime.combine(date.today(), end0) + delta
            if end0.date() != date.today():
                break
            else:
                end0 = end0.time()

        self.fields['start'].choices.sort()




