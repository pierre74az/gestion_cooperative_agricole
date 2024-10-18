# members/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.member_list, name='member_list'),
    path('<int:pk>/', views.member_detail, name='member_detail'),
    path('add/', views.member_create, name='member_create'),
    path('<int:pk>/edit/', views.member_update, name='member_update'),
    path('<int:pk>/delete/', views.member_delete, name='member_delete'),
]
