from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Page d'accueil
    path('contact/', views.contact, name='contact'),  # Page de contact
    path('about/', views.about, name='about'),  # Page à propos
]
