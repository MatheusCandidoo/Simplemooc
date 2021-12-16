from django.urls import path

from . import views

app_name = 'course'

urlpatterns = [
    path('', views.courses, name='index'),
    path('<slug:slug>/', views.details, name='details'),
    path('<slug:slug>/inscricao/', views.enrollment, name='enrollment'),
    path('<slug:slug>/anuncios/', views.announcements, name='announcements'),
    path('<slug:slug>/aulas/', views.show_lessons, name='lessons'),
    path('<slug:slug>/aulas/<int:pk>', views.show_lesson, name='lesson'),
    path('<slug:slug>/materiais/<int:pk>', views.show_material, name='material'),
    path('<slug:slug>/desinscrever/', views.undo_enrollment, name='undo_enrollment'),
    path('<slug:slug>/anuncios/<int:pk>', views.show_announcement, name='show_announcement'),
]