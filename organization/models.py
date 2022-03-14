from django.db import models
from base.models import User
# from staff.models import Employee
# from client.models import Client
# import datetime


class Organization(models.Model):
    # класс для организации
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="own_organisations")
    created = models.DateTimeField(auto_now_add=True)

    """ 
        так как поиск не чувствителен к регистру только для латинского алфавита,
        сделаем удобное для поиска поле name_low
    """
    name_low = models.CharField(max_length=100, default=str(name).lower())

    def __str__(self):
        return str(self.name)


class Service(models.Model):
    name = models.CharField(max_length=64, default="Услуга")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="services")
    description = models.TextField(null=True, blank=True, default="")

    # время, требующееся для выполнения услуги в МИНУТАХ
    time = models.IntegerField(default=15)
    # цена за услугу в РУБЛЯХ
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return str(self.name)


# class Assignment(models.Model):
#     employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="assignments")
#     client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="assignments")
#     service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='assignments')
#
#     # время начала записи
#     date = models.DateField(default=datetime.datetime.now().date())
#     start = models.TimeField(default=datetime.datetime.now().time())