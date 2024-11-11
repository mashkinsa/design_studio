from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from studio.forms import LoginForm, RegistrationForm
from studio.models import UserProfile
from django.shortcuts import render, redirect


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


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
    else:
        form = LoginForm()
    return render(request, 'studio/login.html', {'form': form, 'title': 'Вход'})


@login_required
def profile(request):
    user = request.user
    return render(request, 'studio/profile.html', {'user': user})


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1> Страница не найдена </h1>")




