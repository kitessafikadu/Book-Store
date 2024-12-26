from django.contrib import admin
from .models import Chat

class ChatAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'posted_at')  # Add any fields you want to display in the list view
    search_fields = ('message',)  # Optional: to make messages searchable in the admin

admin.site.register(Chat, ChatAdmin)
