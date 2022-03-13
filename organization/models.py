from django.db import models
from base.models import User


class Organization(models.Model):
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
