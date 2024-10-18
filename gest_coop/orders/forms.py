from django import forms
from .models import CartItem

class AddToCartForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1, initial=1, label='Quantité')
    
    class Meta:
        model = CartItem
        fields = ['quantity']
