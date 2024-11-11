from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
import re


class RegistrationForm(UserCreationForm):
    avatar = forms.ImageField(required=False)
    first_name = forms.CharField(max_length=30, label='Имя', required=True)
    last_name = forms.CharField(max_length=30, label='Фамилия', required=True)
    middle_name = forms.CharField(max_length=30, label='Отчество', required=False)
    consent = forms.BooleanField(label='Согласие на обработку персональных данных', required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'username', 'email', 'avatar', 'password1', 'password2')

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'^[А-ЯЁа-яё\s\-]+$', first_name):
            raise forms.ValidationError("Имя должно содержать только кириллические буквы, пробелы и дефисы.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'^[А-ЯЁа-яё\s\-]+$', last_name):
            raise forms.ValidationError("Фамилия должна содержать только кириллические буквы, пробелы и дефисы.")
        return last_name

    def clean_middle_name(self):
        middle_name = self.cleaned_data.get('middle_name')
        if middle_name and not re.match(r'^[А-ЯЁа-яё\s\-]+$', middle_name):
            raise forms.ValidationError("Отчество должно содержать только кириллические буквы, пробелы и дефисы.")
        return middle_name

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z\-]+$', username):
            raise forms.ValidationError("Логин должен содержать только латиницу и дефисы.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not forms.EmailField().clean(email):
            raise forms.ValidationError("Введите корректный email-адрес.")
        return email






class LoginForm(AuthenticationForm):
    pass


