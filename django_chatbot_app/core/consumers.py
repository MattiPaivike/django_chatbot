import json
import os
import uuid
from channels.generic.websocket import AsyncWebsocketConsumer
from openai import AsyncOpenAI
from .models import ChatConversation
from django.template.loader import render_to_string
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        if self.user.is_authenticated:
            self.messages = await self.fetch_conversation(self.conversation_id)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.save_conversation(self.conversation_id, self.messages)
            # delete conversation if no messages
            if not self.messages:
                await self.delete_conversation(self.conversation_id)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json["message"]

        if not message_text.strip():
            return

        self.messages.append(
            {
                "role": "user",
                "content": message_text,
            }
        )

        user_message_html = render_to_string(
            "websocket_partials/user_message.html",
            {"message_text": message_text},
        )
        await self.send(text_data=user_message_html)

        message_id = uuid.uuid4().hex
        contents_div_id = f"message-response-{message_id}"
        system_message_html = render_to_string(
            "websocket_partials/system_message.html",
            {"contents_div_id": contents_div_id},
        )
        await self.send(text_data=system_message_html)

        client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        stream = await client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL"),
            messages=self.messages,
            stream=True,
        )

        full_message = ""
        async for chunk in stream:
            message_chunk = chunk.choices[0].delta.content
            if message_chunk:
                full_message += message_chunk
                chunk_html = f'<div hx-swap-oob="beforeend:#{contents_div_id}">{message_chunk}</div>'
                await self.send(text_data=chunk_html)

        self.messages.append(
            {
                "role": "assistant",
                "content": full_message,
            }
        )
        final_message = render_to_string(
            "websocket_partials/final_system_message.html",
            {
                "contents_div_id": contents_div_id,
                "message": full_message,
            },
        )
        await client.close()
        await self.send(text_data=final_message)

    @database_sync_to_async
    def fetch_conversation(self, id):
        chat = ChatConversation.objects.get(id=id, user=self.user)
        return chat.conversation if chat.conversation else []

    @database_sync_to_async
    def save_conversation(self, id, new_messages):
        chat = ChatConversation.objects.get(id=id, user=self.user)
        chat.conversation = new_messages
        chat.save()
        
    @database_sync_to_async
    def delete_conversation(self, id):
        try:
            chat = ChatConversation.objects.get(id=id, user=self.user)
            if not chat.conversation:  # Double-checking in case messages were added
                chat.delete()
        except ChatConversation.DoesNotExist:
            pass
