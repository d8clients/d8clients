from django.urls import path
from . import views

urlpatterns = [
    path('', views.organizations_main_page, name="org_main"),
    path('create_org/', views.create_organization, name="create_org"),
    path('search_org/', views.search_organization, name="search_org"),
    path('work_org/', views.organization_work, name="work_org"),
    path('my_subscribes/', views.organization_subscribes, name="org_sub"),
    path('delete_employee/<str:pk>', views.delete_employee, name="delete_employee"),
    path('delete_admin/<str:pk>', views.delete_admin, name="delete_admin"),
    path('service/<str:pk>', views.service_profile, name="service_profile"),
    path('delete_service/<str:pk>', views.delete_service, name="delete_service"),
    path('edit_service/<str:pk>', views.edit_service, name="edit_service"),
    path('<str:pk>/', views.organization_profile, name="org_profile"),
    path('<str:pk>/create_assignment1/', views.create_assignment1, name="create_assignment1"),
    path('<str:pk>/create_assignment2/', views.create_assignment2, name="create_assignment2"),
    path('<str:pk>/edit_mode/', views.organization_edit_mode, name="org_edit"),
    path('<str:pk>/add_employee/', views.add_employee, name="add_employee"),
    path('<str:pk>/add_admin/', views.add_admin, name="add_admin"),
    path('<str:pk>/add_service/', views.add_service, name="add_service"),
]