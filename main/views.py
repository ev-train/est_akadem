from datetime import timezone
from django import template
from django.http import request
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from .models import Photo, Post, Profile, Comment
from .forms import EditAccountForm, EditProfileForm, UserRegisterForm, UserLoginForm, PasswordChangingForm, CommentForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.views import generic, View
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(
                user=user
            )
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрированы.')
            return redirect('/')
        else:
            messages.error(request, 'Ошибка регистрации.')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {"form": form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = UserLoginForm()
    return render(request, 'main/login.html', {"form": form})

def user_logout(request):
    logout(request)
    return redirect('/')

class EditAccountView(generic.UpdateView):
    form_class = EditAccountForm
    template_name = 'main/edit_account.html'
    success_url = reverse_lazy('main:index')

    def get_object(self):
        return self.request.user

class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('main:index')

def password_success(request):
    return render(request, 'main/password_success.html')

class EditProfileView(generic.UpdateView):
    model = Profile
    form_class = EditProfileForm
    template_name = 'main/edit_profile.html'
    success_url = reverse_lazy('main:index')

class ProfileView(generic.DetailView):
    model = Profile
    template_name = 'main/profile.html'
    
    def get_context_data(self, *args, **kwargs):
        users = Profile.objects.all()
        context = super(ProfileView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context["page_user"] = page_user
        user_post_list = Post.objects.filter(post_author = page_user.user).order_by('-post_date')
        context["user_post_list"] = user_post_list
        photo_list = Photo.objects.all()
        context["photo_list"] = photo_list
        return context

def index(request):
    if request.method == 'POST':
        data = request.POST
        post = Post.objects.create(
            post_author = request.user,
            post_text = data['post_text']
        )
        images = request.FILES.getlist('images')
        for image in images:
            photo = Photo.objects.create(
                post=post,
                image=image
            )
        return redirect('/')
    post_list = Post.objects.all().order_by('-post_date')
    post_list_paginator = Paginator(post_list, 5)
    page_num = request.GET.get('page')
    page = post_list_paginator.get_page(page_num)
    context = {
        'page': page,
        'photo_list': Photo.objects.all(),
    }
    return render(request, 'main/index.html', context)

def delete_post(request, pk):
    Post.objects.filter(id=pk).delete()
    return redirect('/')

def delete_comment(request, pk, *args, **kwargs):
    comment = Comment.objects.filter(id=pk)
    post = Post.objects.get(comment__id=pk)
    post_id = post.id
    comment.delete()
    return redirect('main:post', pk=post_id)

def about(request):
    return render(request, 'main/about.html')


class PostView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        photo_list = Photo.objects.all()
        comment_list = Comment.objects.all().order_by('-comment_date')

        context = {
            'post': post,
            'form': form,
            'photo_list': photo_list,
            'comment_list': comment_list
        }

        return render(request, 'main/post.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)
        photo_list = Photo.objects.all()
        comment_list = Comment.objects.all().order_by('-comment_date')

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.comment_author = request.user
            new_comment.comment_post = post
            new_comment.save()
        
        context = {
            'post': post,
            'form': form,
            'photo_list': photo_list,
            'comment_list': comment_list
        }

        return render(request, 'main/post.html', context)


