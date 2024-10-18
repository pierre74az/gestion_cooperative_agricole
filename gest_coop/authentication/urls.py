from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_choice, name='signup'),
    path('signup/buyer/', views.buyer_signup, name='buyer_signup'),
    path('signup/farmer/', views.farmer_signup, name='farmer_signup'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]
