# production_tracking/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.production_list, name='production_list'),
    path('add/', views.production_create, name='production_create'),
    path('<int:pk>/', views.production_detail, name='production_detail'),
    path('<int:pk>/edit/', views.production_update, name='production_update'),
    path('<int:pk>/delete/', views.production_delete, name='production_delete'),
]
