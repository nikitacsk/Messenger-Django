from django.urls import path
from . import views


urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('chat/<int:user_id>/', views.chat_with, name='chat_with'),
    path('chat/<int:user_id>/messages/', views.get_messages, name='get_messages'),

]
