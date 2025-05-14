from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Ruta principal
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/step1/', views.register_step1, name='register_step1'),
    path('register/step2/', views.register_step2, name='register_step2'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
