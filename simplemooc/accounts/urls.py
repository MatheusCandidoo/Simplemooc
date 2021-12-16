from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views


app_name = 'accounts'


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', LoginView.as_view(template_name = 'accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='core:index'), name='logout'),
    path('cadastro/', views.register, name='register'),
    path('editarUsuario/', views.edit, name='edit'),
    path('alterarSenha/', views.edit_password, name='edit_password'),
    path('recuperarSenha/', views.password_reset, name='reset_password'),
    path('confirmarNovaSenha/<str:key>/', views.password_reset_confirm, name='password_reset_confirm'),
]