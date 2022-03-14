from django.db import models
from .models import Service
from staff.models import Employee
from client.models import Client
import datetime


class Assignment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="assignments")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="assignments")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='assignments')

    # время начала записи
    date = models.DateField(default=datetime.datetime.now().date())
    start = models.TimeField(default=datetime.datetime.now().time())

    confirmed = models.BooleanField(default=True)