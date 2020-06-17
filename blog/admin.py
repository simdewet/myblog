from django.contrib import admin
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin
from django import forms

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('text',)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
