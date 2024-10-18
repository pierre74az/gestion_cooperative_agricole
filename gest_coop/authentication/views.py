from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import BuyerSignUpForm, FarmerSignUpForm, CustomAuthenticationForm, UserUpdateForm, FarmerProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser, FarmerProfile

def signup_choice(request):
    return render(request, 'authentication/signup_choice.html')


def signup(request):
    return render(request, 'authentication/signup.html')

def buyer_signup(request):
    if request.method == 'POST':
        form = BuyerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription réussie !")
            return redirect('home')
    else:
        form = BuyerSignUpForm()
    return render(request, 'authentication/buyer_signup.html', {'form': form})

def farmer_signup(request):
    if request.method == 'POST':
        form = FarmerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription réussie !")
            return redirect('home')
    else:
        form = FarmerSignUpForm()
    return render(request, 'authentication/farmer_signup.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Authentifier avec le nom d'utilisateur
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Bienvenue {user.username}!")
                return redirect('home')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe invalide.")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe invalide.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})

def custom_logout(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect('home')




@login_required
def profile(request):
    user = request.user
    if user.user_type == 2:
        try:
            profile = user.farmer_profile
        except FarmerProfile.DoesNotExist:
            profile = FarmerProfile.objects.create(user=user, cultures="")
    else:
        profile = None

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        if user.user_type == 2:
            profile_form = FarmerProfileUpdateForm(request.POST, instance=profile)
        else:
            profile_form = None

        if user_form.is_valid() and (profile_form is None or profile_form.is_valid()):
            user_form.save()
            if profile_form:
                profile_form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès.")
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=user)
        if user.user_type == 2:
            initial_cultures = profile.cultures.split(",") if profile.cultures else []
            profile_form = FarmerProfileUpdateForm(instance=profile, initial={'cultures': initial_cultures})
        else:
            profile_form = None

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'authentication/profile.html', context)
