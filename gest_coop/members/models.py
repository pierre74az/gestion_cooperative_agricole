# members/models.py

from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100, choices=[
        ('manager', 'Gestionnaire'),
        ('worker', 'Ouvrier'),
        ('advisor', 'Conseiller'),
        ('technician', 'Technicien'),
        ('accountant', 'Comptable'),
        ('supervisor', 'Superviseur'),
        ('logistics', 'Logisticien'),
        ('driver', 'Chauffeur'),
        ('trainer', 'Formateur'),
        ('security', 'Sécurité'),
        ('agriculteur', 'Agriculteur'),
    ])
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='members/photos/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_role_display()}"
