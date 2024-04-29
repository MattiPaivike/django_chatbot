from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ChatConversation

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conversations'] = ChatConversation.objects.filter(
            user=self.request.user
        ).exclude(conversation=[])  # Excluding empty conversations
        return context
    
class StartConversationView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        conversation = ChatConversation.objects.create(user=request.user)
        return HttpResponseRedirect(reverse('chat_page', args=[conversation.id]))
    
class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conversation_id = self.kwargs.get('conversation_id')
        if conversation_id:
            conversation = get_object_or_404(ChatConversation, id=conversation_id, user=self.request.user)
            context['conversation'] = conversation
        else:
            context['conversation'] = None
        return context
