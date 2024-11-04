from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('students/', views.student_list, name='student_list'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('enroll/', views.enroll_student, name='enroll_student'),
]
