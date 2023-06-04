from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('/home', views.home, name='home'),
    path('sign-up', views.sign_up, name="sign_up"),
    path('about', views.about, name="about"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/drivers/', views.dashboard_drivers, name='dashboard_drivers'),
    path('dashboard/all', views.dashboard_all, name='dashboard_all'),

    # path('dashboard/all', views.dashboard_all, name='dashboard_all'),

    


]
