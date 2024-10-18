from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import CartItem, Order, OrderItem, Payment
from .forms import AddToCartForm
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
import uuid
import os
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse
from django.core.mail import send_mail

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart_item, created = CartItem.objects.get_or_create(user=user, product=product)
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, f"{product.name} a été ajouté à votre panier.")
            return redirect('product_list')
    else:
        form = AddToCartForm()
    return render(request, 'orders/add_to_cart.html', {'form': form, 'product': product})

@login_required
def view_cart(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    total = sum(item.subtotal() for item in cart_items)
    return render(request, 'orders/view_cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def update_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    if request.method == 'POST':
        form = AddToCartForm(request.POST, instance=cart_item)
        if form.is_valid():
            form.save()
            messages.success(request, f"Le panier a été mis à jour.")
            return redirect('view_cart')
    else:
        form = AddToCartForm(instance=cart_item)
    return render(request, 'orders/update_cart_item.html', {'form': form, 'cart_item': cart_item})

@login_required
def remove_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()
    messages.info(request, f"Le produit a été retiré de votre panier.")
    return redirect('view_cart')



@login_required
def checkout(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    if not cart_items.exists():
        messages.info(request, "Votre panier est vide.")
        return redirect('product_list')
    
    total = sum(item.subtotal() for item in cart_items)
    total_cents = int(total * 100)  # Stripe travaille en cents
    
    if request.method == 'POST':
        try:
            # Créer une session de paiement Stripe
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': item.product.name,
                        },
                        'unit_amount': int(item.product.price * 100),
                    },
                    'quantity': item.quantity,
                } for item in cart_items],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('checkout_success')) + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=request.build_absolute_uri(reverse('view_cart')),
            )
            return redirect(session.url, code=303)
        except Exception as e:
            messages.error(request, f"Une erreur est survenue : {str(e)}")
            return redirect('view_cart')
    
    return render(request, 'orders/checkout.html', {'cart_items': cart_items, 'total': total, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY})


@login_required
def checkout_success(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        messages.error(request, "Session de paiement invalide.")
        return redirect('view_cart')
    
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        user = request.user
        cart_items = CartItem.objects.filter(user=user)
        total = sum(item.subtotal() for item in cart_items)
        
        # Créer une commande
        order = Order.objects.create(user=user, total_price=total, status='completed')
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        order.calculate_total_price()
        
        # Créer un paiement
        payment = Payment.objects.create(order=order, amount=total)
        
        # Générer le reçu PDF
        receipt_html = render_to_string('orders/receipt.html', {'order': order, 'payment': payment})
        receipt_file = f"receipt_{order.id}.pdf"
        receipt_path = os.path.join(settings.MEDIA_ROOT, 'receipts', receipt_file)
        HTML(string=receipt_html).write_pdf(receipt_path)
        payment.receipt = f"receipts/{receipt_file}"
        payment.save()
        
        # Vider le panier
        cart_items.delete()
        
        # Envoyer un email de confirmation
        subject = f"Confirmation de votre commande #{order.id}"
        message = f"Bonjour {user.first_name},\n\nMerci pour votre commande chez GestCoop. Votre commande #{order.id} a été passée avec succès.\n\nTotal : {order.total_price} €\n\nVous pouvez consulter les détails de votre commande dans votre historique de commandes.\n\nCordialement,\nL'équipe GestCoop."
        recipient_list = [user.email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

        messages.success(request, "Votre commande a été passée avec succès ! Un reçu a été généré.")
        return redirect('order_history')
    
        
    except Exception as e:
        messages.error(request, f"Une erreur est survenue : {str(e)}")
        return redirect('view_cart')


@login_required
def order_history(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def view_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/view_order.html', {'order': order})
