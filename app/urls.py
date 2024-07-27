from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('index/',views.index),
    path('notepad/',views.notepad),
]