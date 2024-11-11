from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponseNotFound
from .forms import LoginForm, RegistrationForm
from .models import UserProfile
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm
from .models import LoginAttempt
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

def index(request):
    return render(request, 'studio/index.html')


@login_required
def logout_view(request):
    logout(request)
    print("Вы вышли из системы!")
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                middle_name=form.cleaned_data['middle_name'],
                avatar=form.cleaned_data['avatar']
            )
            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'studio/register.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm
from .models import LoginAttempt
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    is_locked = False

    if request.method == 'POST':
        username = form.data.get('username')
        password = form.data.get('password')

        # Получаем пользователя
        user = User.objects.filter(username=username).first()

        # Проверяем, если пользователь существует
        if user:
            # Получаем или создаем объект LoginAttempt
            login_attempt, created = LoginAttempt.objects.get_or_create(user=user)

            # Проверяем, если пользователь заблокирован
            if login_attempt.attempts >= 2 and timezone.now() < login_attempt.timestamp + timedelta(seconds=5):
                is_locked = True  # Устанавливаем флаг блокировки
                messages.error(request, "Вы заблокированы на 5 секунд после 3 неудачных попыток входа.")
            else:
                # Аутентификация пользователя
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    # Успешный вход
                    login(request, user)
                    login_attempt.attempts = 0  # Сбрасываем попытки
                    login_attempt.timestamp = timezone.now()  # Обновляем время последней попытки
                    login_attempt.save()
                    return redirect('index')
                else:
                    # Неудачная попытка
                    login_attempt.attempts += 1
                    login_attempt.timestamp = timezone.now()  # Обновляем время последней попытки
                    login_attempt.save()
                    messages.error(request, "Неправильный логин или пароль.")
        else:
            messages.error(request, "Пользователь не найден.")

    # Получаем количество попыток входа для отображения в шаблоне
    if request.user.is_authenticated:
        attempts = 0
    else:
        attempts = LoginAttempt.objects.filter(user__username=form.data.get('username')).first()
        attempts = attempts.attempts if attempts else 0

    return render(request, 'studio/login.html', {'form': form, 'login_attempts': attempts, 'is_locked': is_locked})



@login_required
def profile(request):
    user = request.user
    return render(request, 'studio/profile.html', {'user': user})


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1> Страница не найдена </h1>")




