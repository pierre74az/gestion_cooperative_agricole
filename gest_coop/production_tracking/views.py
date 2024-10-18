# production_tracking/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ProductionTracking
from .forms import ProductionTrackingForm
from django.contrib import messages
from .decorators import farmer_required

@farmer_required
def production_list(request):
    production_tracks = ProductionTracking.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'production_tracks': production_tracks,
    }
    return render(request, 'production_tracking/production_list.html', context)

@farmer_required
def production_detail(request, pk):
    production = get_object_or_404(ProductionTracking, pk=pk, user=request.user)
    context = {
        'production': production,
    }
    return render(request, 'production_tracking/production_detail.html', context)

@farmer_required
def production_create(request):
    if request.method == 'POST':
        form = ProductionTrackingForm(request.POST, request.FILES)
        if form.is_valid():
            production = form.save(commit=False)
            production.user = request.user
            production.save()
            messages.success(request, "Suivi de production ajouté avec succès.")
            return redirect('production_list')
    else:
        form = ProductionTrackingForm()
    context = {
        'form': form,
    }
    return render(request, 'production_tracking/production_form.html', context)

@farmer_required
def production_update(request, pk):
    production = get_object_or_404(ProductionTracking, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ProductionTrackingForm(request.POST, request.FILES, instance=production)
        if form.is_valid():
            form.save()
            messages.success(request, "Suivi de production mis à jour avec succès.")
            return redirect('production_detail', pk=production.pk)
    else:
        form = ProductionTrackingForm(instance=production)
    context = {
        'form': form,
        'production': production,
    }
    return render(request, 'production_tracking/production_form.html', context)

@farmer_required
def production_delete(request, pk):
    production = get_object_or_404(ProductionTracking, pk=pk, user=request.user)
    if request.method == 'POST':
        production.delete()
        messages.success(request, "Suivi de production supprimé avec succès.")
        return redirect('production_list')
    context = {
        'production': production,
    }
    return render(request, 'production_tracking/production_confirm_delete.html', context)
