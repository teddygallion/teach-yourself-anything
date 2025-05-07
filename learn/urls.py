from django.urls import path
from .views import load_topic_data
from . import views


app_name="learn"

urlpatterns = [
    path('', views.home, name="home"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('topics/generate/', views.topic_generate, name='topic_generate'),
    path("learning-path/", views.learning_path_view, name="learning_path_view"),
    path('learning-path/save/', views.save_learning_path, name='save_learning_path'),
    path('topics/<int:pk>/edit/', views.edit_topic, name='edit_topic'),
    path('topics/<int:topic_id>/', views.topic_detail, name='topic_detail'),
    path('topics/<int:pk>/delete/', views.delete_topic_confirm, name='delete_topic_confirm'),
    path('topics/<int:pk>/delete/confirm/', views.delete_topic, name='delete_topic'),
    path('topics/<int:topic_id>/modules/<int:module_id>/', views.module_detail, name='module_detail'),
    path('topics/<int:topic_id>/modules/<int:module_id>/lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('load-topic-data/', load_topic_data, name='load-topic-data'),
]
