from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def farmer_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 2:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Accès refusé. Cette section est réservée aux agriculteurs.")
            return redirect('home')  # Assurez-vous que 'home' est une URL valide
    return _wrapped_view
