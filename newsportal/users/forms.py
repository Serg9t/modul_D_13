from allauth.account.forms import SignupForm

from django.contrib.auth.models import Group
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.mail import send_mail, EmailMultiAlternatives, mail_managers, mail_admins


from django.contrib.auth.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={
        'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите имя пользователя'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите имя'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите фамилию'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите emalil'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)

        mail_admins(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте.'
        )

        return user


# class CustomSignupForm(SignupForm):
#     def save(self, request):
#         user = super().save(request)
#
#         subject = 'Добро пожаловать на наш новостной сайт!'
#         text = f'{user.username}, вы успешно зарегистрировались на сайте!'
#         html = (
#             f'<b>{user.username}</b>, вы успешно зарегистрировались на '
#             f'<a href="http://127.0.0.1:8000">сайте</a>!'
#         )
#         msg = EmailMultiAlternatives(
#             subject=subject, body=text, from_email=None, to=[user.email]
#         )
#         msg.attach_alternative(html, "text/html")
#         msg.send()
#
#         return user

# class CustomSignupForm(SignupForm):
#     def save(self, request):
#         user = super().save(request)
#         common_users = Group.objects.get(name="common users")
#         user.groups.add(common_users)
#         return user
