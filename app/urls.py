from django.urls import path
from . import views
from . import authentication


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('question_maker/', views.question_maker, name='question_maker'),
    path('verify_otp/', authentication.verify_otp, name='verify_otp'),
    path('index/',views.index),
    path('notepad/<int:question_id>/',views.notepad, name='notepad'),
    path('signin/',authentication.signin,name='signin'),
    path('signup/',authentication.signup,name='signup'),
    path('forms_submit/<int:question_id>/', views.process_textarea, name='forms_submit'),
]