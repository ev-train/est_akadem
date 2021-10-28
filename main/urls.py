from django import template
from django.urls import path
from . import views
from .views import PasswordChangeView, PostView, delete_post, delete_comment

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('delete_post/<int:pk>/', views.delete_post, name='delete_post'),
    path('delete_comment/<int:pk>/', views.delete_comment, name='delete_comment'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('edit_account/', views.EditAccountView.as_view(), name='edit_account'),
    path('password/', PasswordChangeView.as_view(template_name='main/change_password.html')),
    path('password_success/', views.password_success, name='password_success'),
    path('edit_profile/<int:pk>/', views.EditProfileView.as_view(), name='edit_profile'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('post/<int:pk>/', PostView.as_view(), name='post'),
]