from django.urls import path
from . import views

urlpatterns = [
    
    path("registration/", views.registration, name="registration"),
    path("login/", views.custom_login, name="login"),
    path("logout/", views.custom_logout, name="logout"),
    
    
    
]
