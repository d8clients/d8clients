from django.contrib import admin
from .models import Organization, Service
from .assign_model import Assignment

admin.site.register(Organization)
admin.site.register(Service)
admin.site.register(Assignment)