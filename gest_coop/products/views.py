from django.shortcuts import render
from django.db import models
from .models import Product
from django.contrib.auth.decorators import login_required

@login_required
def product_list(request):
    user = request.user
    if user.user_type == 1:  # Acheteur
        category_choices = ['cereals', 'vegetables']
    elif user.user_type == 2:  # Agriculteur
        category_choices = ['seeds', 'fertilizers']
    else:
        category_choices = []

    # Filtrer les catégories disponibles pour l'utilisateur
    categories = Product.objects.filter(category__in=category_choices).values_list('category', 'category').distinct()

    # Créer un dictionnaire pour les noms de catégories
    category_dict = dict(Product.CATEGORY_CHOICES)
    filtered_categories = [(cat, category_dict.get(cat, cat)) for cat in category_choices]

    # Récupérer les filtres de la requête GET
    category = request.GET.get('category')
    search_query = request.GET.get('search', '')

    # Filtrer les produits par catégorie si spécifié
    if category and category in category_choices:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.filter(category__in=category_choices)

    # Filtrer les produits par recherche si spécifié
    if search_query:
        products = products.filter(
            models.Q(name__icontains=search_query) | models.Q(description__icontains=search_query)
        )

    context = {
        'products': products,
        'filtered_categories': filtered_categories,
        'search_query': search_query,
    }
    return render(request, 'products/product_list.html', context)
