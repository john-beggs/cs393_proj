"""
URL configuration for fitness_proj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from fitness_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/receptionist/', views.dashboard, name='receptionist_dashboard'),
    path('dashboard/manager/', views.dashboard, name='manager_dashboard'),
    path('dashboard/trainer/', views.dashboard, name='trainer_dashboard'),
    path('dashboard/member/', views.dashboard, name='member_dashboard'),
    path('register-member/', views.register_member, name='register_member'),
    path('schedule-training-session/', views.schedule_training_session, name='schedule_training_session'),
    path('update-goals/<int:member_id>/', views.update_goals, name='update_goals'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('log-food-intake/', views.log_food_intake, name='log_food_intake'),
    path('food-summary/', views.food_summary, name='food_summary'),
    path('get-descriptions/', views.get_descriptions, name='get_descriptions'),
    path('member-list/', views.member_list, name='member_list'),
    path('member-report/', views.member_report, name='member_report'),
    path('track-payment/', views.track_payment, name='track_payment'),
    path('update-payment/<int:payment_id>/', views.update_payment, name='update_payment'),
    path('view-fines/<int:member_id>/', views.view_fines, name='view_fines'),
]

