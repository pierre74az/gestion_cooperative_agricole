# production_tracking/admin.py

from django.contrib import admin
from .models import ProductionTracking

@admin.register(ProductionTracking)
class ProductionTrackingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'type_culture',
        'region',
        'province',
        'date_recolte',
        'quantite_engrais',
        'date_mise_engrais',
        'created_at',
        'updated_at',
    )
    list_filter = ('type_culture', 'region', 'province', 'date_recolte', 'date_mise_engrais')
    search_fields = ('user__username', 'region', 'province', 'type_culture')
    readonly_fields = ('created_at', 'updated_at')
