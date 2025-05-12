from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('verify/', views.verify_email, name='verify_email'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
