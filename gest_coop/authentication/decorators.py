from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def buyer_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 1:
            return function(request, *args, **kwargs)
        else:
            messages.error(request, "Accès refusé. Cette section est réservée aux acheteurs.")
            return redirect('home')
    return wrap

def farmer_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 2:
            return function(request, *args, **kwargs)
        else:
            messages.error(request, "Accès refusé. Cette section est réservée aux agriculteurs.")
            return redirect('home')
    return wrap
