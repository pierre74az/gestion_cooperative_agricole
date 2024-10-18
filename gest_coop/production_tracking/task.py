from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from .models import ProductionTracking
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def update_production_tracking():
    """
    Cette tâche Celery vérifie les suivis de production en fonction des dates d'engrais et de récolte.
    Elle envoie des notifications ou met à jour les statuts des productions en cours.
    """
    today = timezone.now().date()

    # Filtrer les suivis de production en fonction de la date d'engrais et de récolte
    productions = ProductionTracking.objects.filter(
        date_mise_engrais__lte=today,  # Les productions où la date de mise d'engrais est passée ou est aujourd'hui
        date_recolte__gte=today,       # Les productions où la date de récolte n'est pas encore passée
    )

    for production in productions:
        agriculteur = production.agriculteur

        # 1. Gestion de la mise d'engrais
        if today >= production.date_mise_engrais:
            production.status = 'Engrais Applied'  # Par exemple, statut "Engrais appliqué"
            production.save()

            # Envoi d'une notification de rappel pour l'application d'engrais
            if today == production.date_mise_engrais:
                send_mail(
                    'Rappel : Application de l\'engrais',
                    f'Bonjour {agriculteur.username},\n\n'
                    f'Il est temps d\'appliquer l\'engrais pour votre culture de {production.type_culture}.\n\n'
                    'Merci,\nL\'équipe de suivi de production',
                    'noreply@gestcoop.com',
                    [agriculteur.email],
                    fail_silently=False,
                )

        # 2. Gestion de la récolte
        if today >= production.date_recolte:
            production.status = 'Ready for Harvest'  # Par exemple, statut "Prêt pour la récolte"
            production.save()

            # Envoi d'un email de rappel pour la récolte imminente
            if today >= production.date_recolte - timezone.timedelta(days=7):  # Récolte dans 7 jours
                send_mail(
                    'Rappel de Récolte Imminente',
                    f'Bonjour {agriculteur.username},\n\n'
                    f'Votre production de {production.type_culture} sera prête pour la récolte bientôt. '
                    f'Veuillez planifier les actions nécessaires.\n\n'
                    'Merci,\nL\'équipe de suivi de production',
                    'noreply@gestcoop.com',
                    [agriculteur.email],
                    fail_silently=False,
                )
