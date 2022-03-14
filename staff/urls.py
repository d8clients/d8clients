from django.urls import path
from . import views

urlpatterns = [
    path('edit_employee/<str:pk>', views.edit_employee, name="edit_employee"),
    path('edit_timetable/<str:pk>', views.edit_timetable, name="edit_timetable"),
    path('<str:pk>', views.employee_profile, name="employee_profile")
]