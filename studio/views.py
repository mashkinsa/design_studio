from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from .models import DesignRequest, Category, UserProfile
from .forms import DesignRequestForm, LoginForm, RegistrationForm, CategoryForm
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


def main(request):
    # Получаем 4 последние выполненные заявки
    completed_requests = DesignRequest.objects.filter(status='completed').order_by('-created_at')[:4]

    # Считаем количество заявок в статусе 'Принято в работу'
    in_progress_count = DesignRequest.objects.filter(status='in_progress').count()
    return render(request, 'studio/main.html', {
        'completed_requests': completed_requests,
        'in_progress_count': in_progress_count,
    })




@login_required
def logout_view(request):
    logout(request)
    print("Вы вышли из системы!")
    return redirect('main')


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
                messages.error(request, "Вы заблокированы на 5 минут после 3 неудачных попыток входа.")
            else:
                # Аутентификация пользователя
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    # Успешный вход
                    login(request, user)
                    login_attempt.attempts = 0  # Сбрасываем попытки
                    login_attempt.timestamp = timezone.now()  # Обновляем время последней попытки
                    login_attempt.save()
                    return redirect('main')
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


@login_required
def create_request(request):
    if request.method == 'POST':
        form = DesignRequestForm(request.POST, request.FILES)
        if form.is_valid():
            design_request = form.save(commit=False)
            design_request.user = request.user  # Устанавливаем текущего пользователя
            design_request.save()
            return redirect('view_requests')
    else:
        form = DesignRequestForm()
    return render(request, 'studio/create_request.html', {'form': form})


def view_requests(request):
    status_filter = request.GET.get('status', None)
    sort_complexity = request.GET.get('sort_complexity', 'asc')

    requests = DesignRequest.objects.filter(user=request.user)

    if status_filter:
        requests = requests.filter(status=status_filter)

    # Сортировка по сложности
    if sort_complexity == 'desc':
        requests = requests.order_by('-complexity')  # От сложной к легкой
    else:
        requests = requests.order_by('complexity')  # От легкой к сложной

    return render(request, 'studio/view_requests.html', {'requests': requests})


def delete_request(request, request_id):
    request_to_delete = get_object_or_404(DesignRequest, id=request_id)

    if request.method == 'POST':
        request_to_delete.delete()
        return redirect('view_requests')  # Перенаправление на страницу с заявками

    return render(request, 'studio/delete_request.html', {'request': request_to_delete})

