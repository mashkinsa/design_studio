from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    first_name = models.CharField(max_length=30, blank=True)  # Имя
    last_name = models.CharField(max_length=30, blank=True)   # Фамилия
    middle_name = models.CharField(max_length=30, blank=True)  # Отчество
    avatar = models.ImageField(upload_to='user_avatars', blank=True)

    def __str__(self):
        return f'{self.user} Profile'


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class DesignRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Принято в работу'),
        ('completed', 'Выполнено'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='design_requests')
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Изменено на ForeignKey
    photo = models.ImageField(upload_to='design_photos/')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    comment = models.TextField(blank=True, null=True)
    complexity = models.IntegerField(default=0)  # Поле для сложности заявки

    def save(self, *args, **kwargs):
        # Вычисляем сложность на основе длины описания
        self.complexity = len(self.description)  # Можно использовать любую другую логику
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title


class LoginAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    attempts = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - {self.attempts} attempts at {self.timestamp}'