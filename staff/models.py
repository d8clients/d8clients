from django.db import models
from base.models import User
from organization.models import Organization, Service


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='employees')
    bio = models.TextField(null=True, blank=True, default="")

    # услуги, которые может предоставить исполнитель
    services = models.ManyToManyField(Service, related_name="employees", blank=True)

    # принял ли пользователь заявку
    confirmed = models.BooleanField(default='True')

    def __str__(self):
        return self.user.get_full_name()


class Admin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='admins')
    is_host = models.BooleanField(default=False)

    # принял ли пользователь заявку
    confirmed = models.BooleanField(default='True')

    def __str__(self):
        return self.user.get_full_name()


class WorkDay(models.Model):
    """
        тип данных, отвечающий за рабочие часы сотрудника
        в определенный день
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="workdays")
    date = models.DateField()

