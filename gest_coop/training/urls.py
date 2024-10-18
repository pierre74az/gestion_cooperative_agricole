from django.urls import path
from . import views

urlpatterns = [
    path('', views.training_dashboard, name='training_dashboard'),
    path('<int:formation_id>/', views.formation_detail, name='formation_detail'),
    path('<int:formation_id>/enroll/', views.enroll_formation, name='enroll_formation'),
    path('<int:formation_id>/start/', views.start_formation, name='start_formation'),
    path('history/', views.user_formation_history, name='user_formation_history'),
]
