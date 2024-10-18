from django.contrib import admin
from .models import Formation, Quiz, Question, Choice, UserFormation, UserAnswer

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

class QuizInline(admin.StackedInline):
    model = Quiz
    extra = 0

@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    inlines = [QuizInline]
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'formation')
    search_fields = ('title', 'formation__title')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz')
    search_fields = ('text', 'quiz__title')

@admin.register(UserFormation)
class UserFormationAdmin(admin.ModelAdmin):
    list_display = ('user', 'formation', 'completed', 'started_at', 'completed_at')
    list_filter = ('completed', 'started_at', 'completed_at')
    search_fields = ('user__username', 'formation__title')

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'choice')
    list_filter = ('question', 'choice')
    search_fields = ('user__username', 'question__text', 'choice__text')
