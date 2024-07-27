from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('question_maker/', views.question_maker, name='question_maker'),
    path('index/',views.index),
    path('notepad/',views.notepad, name='notepad'),
    path('signin/',views.signin),
    path('signup/',views.signup),
]