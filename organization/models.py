from django.db import models
from base.models import User


class Organization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="own_organisations")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)
