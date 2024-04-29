from django.urls import path
from core import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('start/', views.StartConversationView.as_view(), name='start_new_conversation'),
    path('chat/<uuid:conversation_id>/', views.ChatView.as_view(), name='chat_page'),
]