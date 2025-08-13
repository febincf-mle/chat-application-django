from django.urls import path
from . import views


app_name = "auth"

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register_user, name='register'),
]