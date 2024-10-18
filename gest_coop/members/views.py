# members/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Member
from .forms import MemberForm
from django.contrib import messages
from django.core.exceptions import PermissionDenied

# Fonction de vérification pour administrateurs
def admin_required(user):
    return user.is_staff

# Fonction de vérification pour agriculteurs
def farmer_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user = request.user  # Récupère l'utilisateur de la requête
        if user.is_authenticated and hasattr(user, 'user_type') and user.user_type == 2:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied  # Lève une erreur si l'utilisateur n'est pas un agriculteur
    return _wrapped_view

# Liste des membres accessible aux agriculteurs et administrateurs
@login_required
@farmer_required
def member_list(request):
    members = Member.objects.all()
    context = {
        'members': members,
    }
    return render(request, 'members/member_list.html', context)

# Détails d'un membre accessible aux agriculteurs et administrateurs
@login_required
@farmer_required
def member_detail(request, pk):
    member = get_object_or_404(Member, pk=pk)
    context = {
        'member': member,
    }
    return render(request, 'members/member_detail.html', context)

# Ajouter un membre (accessible uniquement aux administrateurs)
@login_required
@user_passes_test(admin_required)
def member_create(request):
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Membre ajouté avec succès.")
            return redirect('member_list')
    else:
        form = MemberForm()
    context = {
        'form': form,
    }
    return render(request, 'members/member_form.html', context)

# Modifier un membre (accessible uniquement aux administrateurs)
@login_required
@user_passes_test(admin_required)
def member_update(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, "Membre mis à jour avec succès.")
            return redirect('member_detail', pk=member.pk)
    else:
        form = MemberForm(instance=member)
    context = {
        'form': form,
        'member': member,
    }
    return render(request, 'members/member_form.html', context)

# Supprimer un membre (accessible uniquement aux administrateurs)
@login_required
@user_passes_test(admin_required)
def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        member.delete()
        messages.success(request, "Membre supprimé avec succès.")
        return redirect('member_list')
    context = {
        'member': member,
    }
    return render(request, 'members/member_confirm_delete.html', context)
