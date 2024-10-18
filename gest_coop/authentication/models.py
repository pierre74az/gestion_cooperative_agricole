from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Acheteur'),
        (2, 'Agriculteur'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)

    def __str__(self):
        return self.username

class FarmerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='farmer_profile')
    # Types de cultures (max 5)
    CULTURE_CHOICES = [
        ('sésame', 'Sésame'),
    ('maïs', 'Maïs'),
    ('mil', 'Mil'),
    ('sorgho', 'Sorgho'),
    ('coton', 'Coton'),
    ('arachide', 'Arachide'),
    ('tomate', 'Tomate'),
    ('melon', 'Melon'),
    ]
    cultures = models.CharField(max_length=255)  # Stocke les cultures sélectionnées sous forme de chaîne

    def __str__(self):
        return f"{self.user.username} - Profile Agriculteur"
