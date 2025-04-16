# comments/admin.py
from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'text', 'created_at')  # Уберите 'likes' и 'dislikes'

admin.site.register(Comment, CommentAdmin)
