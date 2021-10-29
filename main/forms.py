'''from .models import Post, Photo'''
from django import forms
from django.forms import ModelForm, fields, TextInput, widgets, Textarea, ImageField, FileInput
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm, UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, Comment

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class EditAccountForm(UserChangeForm):
    username = forms.CharField(label='Измените логин:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Измените E-mail:', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email')

class EditProfileForm(ModelForm):
    profile_pic = forms.ImageField(label='Фото профиля:', widget=forms.FileInput(attrs={'class': 'form-control', }), required=False)
    bio = forms.CharField(label='О себе:', widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    website_url = forms.CharField(label='Личный сайт:', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    inst_url = forms.CharField(label='Instagram:', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    vk_url = forms.CharField(label='Vk:', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Profile
        fields = ['profile_pic', 'bio', 'website_url', 'inst_url', 'vk_url']

class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))
    new_password2 = forms.CharField(label='Повторите новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

class CommentForm(forms.ModelForm):
    comment_text = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'rows':3}))

    class Meta:
        model = Comment
        fields = ['comment_text']
