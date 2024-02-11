from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'message', 'is_read', 'date')
    list_filter = ('is_read', 'date')
    search_fields = ('sender__email', 'receiver__email', 'message')