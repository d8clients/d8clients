from django.urls import path
from . import views

urlpatterns = [
    path('', views.organizations_main_page, name="org_main"),
    path('create_org', views.create_organization, name="create_org")
]