from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('topics/generate/', views.topic_generate, name='topic_generate'),
    path('topics/<int:topic_id>/', views.topic_detail, name='topic_detail'),
    path('topics/<int:topic_id>/modules/<int:module_id>/', views.module_detail, name='module_detail'),
    path('topics/<int:topic_id>/modules/<int:module_id>/lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
]
