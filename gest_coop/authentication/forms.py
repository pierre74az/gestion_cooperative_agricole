from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, FarmerProfile


class BuyerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'phone_number', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 1  # Acheteur
        if commit:
            user.save()
        return user

class FarmerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
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

    cultures = forms.MultipleChoiceField(
        choices=CULTURE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'phone_number', 'email', 'password1', 'password2', 'cultures')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 2  # Agriculteur
        if commit:
            user.save()
            # Sauvegarde du profil agriculteur
            cultures = self.cleaned_data.get('cultures')
            FarmerProfile.objects.create(user=user, cultures=",".join(cultures))
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Nom d\'utilisateur ou Email ou Numéro de Téléphone')




class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone_number')

class FarmerProfileUpdateForm(forms.ModelForm):
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

    cultures = forms.MultipleChoiceField(
        choices=CULTURE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = FarmerProfile
        fields = ('cultures',)

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.cultures = ",".join(self.cleaned_data.get('cultures'))
        if commit:
            profile.save()
        return profile
