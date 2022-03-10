from django import forms
from .models import User
from .validate import validate_password, validate_name


# форма для входа пользователя в систему
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


# форма для регистрации нового пользователя
class UserRegistrationForm(forms.ModelForm):
    name = forms.CharField(label='Имя', max_length=64, min_length=1)
    surname = forms.CharField(label='Фамилия', max_length=64, min_length=1)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    business_only = forms.BooleanField(label='Создать аккаунт только для работы', required=False, initial=False)

    # форма связана с моделью User
    class Meta:
        model = User
        fields = ['name', 'surname', 'email', 'business_only', 'password']

    def clean_name(self):
        # проверка имени на корректность
        valid_err = validate_name(self.cleaned_data, 'name')
        if valid_err:
            raise forms.ValidationError(valid_err)
        return self.cleaned_data['name']

    def clean_surname(self):
        # проверка фамилии на корректность
        valid_err = validate_name(self.cleaned_data, 'surname')
        if valid_err:
            raise forms.ValidationError(valid_err)
        return self.cleaned_data['surname']

    def clean_email(self):
        # проверка email на уникальность
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким e-mail уже существует')
        return email

    def clean(self):
        # проверка пароля на выполнение требований
        valid_err = validate_password(self.cleaned_data)

        # вызов всех найденных функцией validate_password ошибок
        if valid_err:
            raise forms.ValidationError(valid_err)


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput, required=False)
    password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Повторите новый пароль', widget=forms.PasswordInput, required=False)

    def clean(self):
        # проверка нового пароля на выполнение требований
        valid_err = validate_password(self.cleaned_data)

        # вызов всех найденных функцией validate_password ошибок
        if valid_err:
            raise forms.ValidationError(valid_err)


class UserChangeForm(forms.ModelForm):
    name = forms.CharField(label='Имя', max_length=64, min_length=1)
    surname = forms.CharField(label='Фамилия', max_length=64, min_length=1)

    class Meta:
        model = User
        fields = ['name', 'surname']

    def clean_name(self):
        # проверка имени на корректность
        valid_err = validate_name(self.cleaned_data, 'name')
        if valid_err:
            raise forms.ValidationError(valid_err)
        return self.cleaned_data['name']

    def clean_surname(self):
        # проверка фамилии на корректность
        valid_err = validate_name(self.cleaned_data, 'surname')
        if valid_err:
            raise forms.ValidationError(valid_err)
        return self.cleaned_data['surname']
