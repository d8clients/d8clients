from django.db import models
from base.models import User
from organization.models import Organization
# Create your models here.


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client', null=False)

    subscribes = models.ManyToManyField(Organization, related_name="subscribers", blank=True)

    def __str__(self):
        return self.user.get_full_name()