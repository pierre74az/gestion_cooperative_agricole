
from django.db import models
from django.conf import settings

class ProductionTracking(models.Model):
    CULTURE_CHOICES = [
        ('sésame', 'Sésame'),
        ('maïs', 'Maïs'),
        ('mil', 'Mil'),
        ('sorgho', 'Sorgho'),
        ('riz', 'Riz'),
        ('arachide', 'Arachide'),
        ('coton', 'Coton'),
        ('niébé', 'Niébé'),
        ('gombo', 'Gombo'),
        ('tomate', 'Tomate'),
        ('oignon', 'Oignon'),
        ('igname', 'Igname'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='production_tracks'
    )
    region = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    type_culture = models.CharField(max_length=50, choices=CULTURE_CHOICES)
    date_prevue_semer = models.DateField(null=True, blank=True)
    date_mise_engrais = models.DateField(null=True, blank=True)
    quantite_engrais = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Quantité d'engrais en kg"
    )
    date_recolte = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.type_culture} - {self.user.username} ({self.region}, {self.province})"
