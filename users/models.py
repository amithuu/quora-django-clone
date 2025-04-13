from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, unique=True)
    
    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'auth_user'
        

class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name='questions')
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tbl_questions'



class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.user.username} on {self.question.title}"

    class Meta:
        db_table = 'tbl_answers'
        
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'answer')  # user can like an answer only once
        db_table = 'tbl_likes'

    def __str__(self):
        return f"{self.user.username} liked {self.answer.id}"