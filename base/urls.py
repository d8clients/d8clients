from django.urls import path, include
from . import views

urlpatterns = [
    path('clients/', include('client.urls')),
    path('business/', include('staff.urls')),
    path('organization/', include('organization.urls')),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_page, name="logout"),
    path('', views.main, name="main"),
    path('about/', views.about_us, name="about_us"),
    path('registration/', views.registration_page, name="registration"),
    path('change_password/', views.change_password, name="change_password"),
    path('change_role/', views.change_role, name="change_role"),
    path('change_user_info/', views.change_user_info, name="change_user_info")
]


