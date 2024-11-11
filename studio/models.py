from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    first_name = models.CharField(max_length=30, blank=True)  # Имя
    last_name = models.CharField(max_length=30, blank=True)   # Фамилия
    middle_name = models.CharField(max_length=30, blank=True)  # Отчество
    avatar = models.ImageField(upload_to='user_avatars', blank=True)

    def __str__(self):
        return f'{self.user} Profile'


