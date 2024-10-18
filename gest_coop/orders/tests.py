from django.test import TestCase
from django.contrib.auth import get_user_model
from products.models import Product
from .models import CartItem, Order, OrderItem, Payment

User = get_user_model()

class OrderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123', user_type=1)
        self.product1 = Product.objects.create(name='Céréale 1', category='cereals', description='Description 1', price=10.00)
        self.product2 = Product.objects.create(name='Légume 1', category='vegetables', description='Description 2', price=5.00)
    
    def test_add_to_cart(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(f'/orders/add/{self.product1.id}/', {'quantity': 2})
        self.assertEqual(response.status_code, 302)  # Redirection après ajout
        cart_item = CartItem.objects.get(user=self.user, product=self.product1)
        self.assertEqual(cart_item.quantity, 2)
    
    def test_checkout(self):
        self.client.login(username='testuser', password='password123')
        # Ajouter des produits au panier
        CartItem.objects.create(user=self.user, product=self.product1, quantity=2)
        CartItem.objects.create(user=self.user, product=self.product2, quantity=3)
        response = self.client.post('/orders/checkout/')
        self.assertEqual(response.status_code, 302)  # Redirection vers Stripe
        # Vérifier que la commande a été créée
        order = Order.objects.get(user=self.user)
        self.assertEqual(order.total_price, 35.00)
        # Vérifier que le panier a été vidé
        cart_items = CartItem.objects.filter(user=self.user)
        self.assertFalse(cart_items.exists())
