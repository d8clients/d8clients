from django.urls import path
from . import views

urlpatterns = [
    path('', views.organizations_main_page, name="org_main"),
    path('create_org/', views.create_organization, name="create_org"),
    path('search_org/', views.search_organization, name="search_org"),
    path('work_org/', views.organization_work, name="work_org"),
    path('my_subscribes/', views.organization_subscribes, name="org_sub"),
    path('<str:pk>/', views.organization_profile, name="org_profile"),
    path('<str:pk>/edit_mode/', views.organization_edit_mode, name="org_edit"),
    path('<str:pk>/add_employee/', views.add_employee, name="add_employee"),
    path('<str:pk>/add_admin/', views.add_admin, name="add_admin"),
    path('delete_employee/<str:pk>', views.delete_employee, name="delete_employee"),
    path('delete_admin/<str:pk>', views.delete_admin, name="delete_admin")
]