from django.shortcuts import redirect

def farmer_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user = request.user  # Récupère l'utilisateur de la requête
        if user.is_authenticated and user.user_type == 2:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')  # Assurez-vous que 'home' est une URL valide
    return _wrapped_view
