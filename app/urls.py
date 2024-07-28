from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('question_maker/', views.question_maker, name='question_maker'),
    path('index/',views.index),
    path('notepad/<int:question_id>/',views.notepad, name='notepad'),
    path('signin/',views.signin,name='signin'),
    path('signup/',views.signup,name='signup'),
    path('forms_submit/<int:question_id>/', views.process_textarea, name='forms_submit'),
]