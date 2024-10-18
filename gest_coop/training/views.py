from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Formation, UserFormation, Quiz, Question, Choice, UserAnswer
from django.contrib import messages
from django.utils import timezone
from .forms import QuizForm
from .decorators import farmer_required


@farmer_required
def formation_list(request):
    formations = Formation.objects.all()
    user_formations = UserFormation.objects.filter(user=request.user).values_list('formation_id', flat=True)
    context = {
        'formations': formations,
        'user_formations': user_formations,
    }
    return render(request, 'training/formation_list.html', context)

@farmer_required
def formation_detail(request, formation_id):
    formation = get_object_or_404(Formation, id=formation_id)
    user_has_formation = UserFormation.objects.filter(user=request.user, formation=formation).exists()
    user_formation = None

    if user_has_formation:
        user_formation = UserFormation.objects.get(user=request.user, formation=formation)

    context = {
        'formation': formation,
        'user_has_formation': user_has_formation,
        'user_formation': user_formation,
    }
    return render(request, 'training/formation_detail.html', context)

@farmer_required
def enroll_formation(request, formation_id):
    formation = get_object_or_404(Formation, id=formation_id)
    user_formation, created = UserFormation.objects.get_or_create(user=request.user, formation=formation)
    if created:
        messages.success(request, f"Vous êtes inscrit à la formation '{formation.title}'.")
    else:
        messages.info(request, f"Vous êtes déjà inscrit à la formation '{formation.title}'.")
    return redirect('formation_detail', formation_id=formation.id)

@farmer_required
def start_formation(request, formation_id):
    formation = get_object_or_404(Formation, id=formation_id)
    user_formation = get_object_or_404(UserFormation, user=request.user, formation=formation)
    if user_formation.completed:
        messages.info(request, "Vous avez déjà complété cette formation.")
        return redirect('formation_detail', formation_id=formation.id)
    quiz = get_object_or_404(Quiz, formation=formation)
    if request.method == 'POST':
        form = QuizForm(request.POST, quiz=quiz)
        if form.is_valid():
            user_answers = []
            for question in quiz.questions.all():
                selected_choice = form.cleaned_data.get(f'question_{question.id}')
                if selected_choice:
                    choice = Choice.objects.get(id=selected_choice)
                    UserAnswer.objects.create(user=request.user, question=question, choice=choice)
                    user_answers.append((question, choice))
            # Vérifier les réponses
            correct_answers = 0
            total_questions = quiz.questions.count()
            for question, choice in user_answers:
                if choice.is_correct:
                    correct_answers += 1
            score = (correct_answers / total_questions) * 100
            if score >= 70:  # Seuil de réussite
                user_formation.completed = True
                user_formation.completed_at = timezone.now()
                user_formation.save()
                messages.success(request, "Félicitations ! Vous avez complété la formation avec succès.")
            else:
                messages.error(request, "Votre score est insuffisant. Veuillez réessayer.")
            context = {
                'formation': formation,
                'quiz': quiz,
                'score': score,
                'correct_answers': correct_answers,
                'total_questions': total_questions,
            }
            return render(request, 'training/quiz_result.html', context)
    else:
        form = QuizForm(quiz=quiz)
    context = {
        'formation': formation,
        'quiz': quiz,
        'form': form,
    }
    return render(request, 'training/start_formation.html', context)

@farmer_required
def user_formation_history(request):
    user_formations = UserFormation.objects.filter(user=request.user).order_by('-started_at')
    context = {
        'user_formations': user_formations,
    }
    return render(request, 'training/user_formation_history.html', context)



@login_required
@farmer_required
def training_dashboard(request):
    formations = Formation.objects.all()
    user_formations = UserFormation.objects.filter(user=request.user).order_by('-started_at')
    
    # Créez un ensemble des IDs de formations pour une recherche facile dans le template
    user_formation_ids = set(user_formations.values_list('formation_id', flat=True))
    
    context = {
        'formations': formations,
        'user_formations': user_formations,
        'user_formation_ids': user_formation_ids,  # Passez l'ensemble au contexte
    }
    return render(request, 'training/dashboard.html', context)
