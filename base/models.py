from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


# модифицированная встроенная модель пользователя
class User(AbstractUser):

    # искуственно удаляем поле username, приравнивая его к None
    username = None

    # обязательные поля для пользователей
    email = models.EmailField(unique=True, default='')
    name = models.CharField(max_length=64, default='')
    surname = models.CharField(max_length=64, default='')

    # флаг, показывающий, есть ли у пользователя функционал клиента
    business_only = models.BooleanField(default=False, blank=True)

    # авторизация происходит по почте, а не по имени пользователя
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    # модифицированный встроенный менеджер
    objects = UserManager()

    @property
    def is_client(self):
        return not self.business_only

    @property
    def is_admin(self):
        return bool(self.admin.count())

    @property
    def is_employee(self):
        return bool(self.employee.count())

    @property
    def is_staff(self):
        return self.is_admin or self.is_employee

    def __str__(self):
        return str(self.name) + ' ' + str(self.surname)

    def get_short_name(self):
        return self.name

    def get_full_name(self):
        return str(self.name) + ' ' + str(self.surname)
