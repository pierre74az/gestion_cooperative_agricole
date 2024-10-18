from django.db import models

class Formation(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    pdf = models.FileField(upload_to='formations/pdfs/', null=True, blank=True)
    video = models.FileField(upload_to='formations/videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Quiz(models.Model):
    formation = models.OneToOneField(Formation, on_delete=models.CASCADE, related_name='quiz')
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return f"Quiz pour {self.formation.title}"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    
    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text

from django.contrib.auth import get_user_model

User = get_user_model()

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} a répondu à '{self.question.text}'"

class UserFormation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_formations')
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name='user_formations')
    completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.formation.title}"
