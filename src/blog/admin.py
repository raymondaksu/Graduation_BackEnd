from django.contrib import admin
from django.db import models
import nested_admin
from .models import Category, Post, Comment, Like, PostView

class PostViewInline(nested_admin.NestedTabularInline):
    model = PostView
    classes = ['collapse']

class LikeInline(nested_admin.NestedTabularInline):
    model = Like
    classes = ['collapse']

class CommentInline(nested_admin.NestedTabularInline):
    model = Comment
    classes = ['collapse']

class PostAdmin(nested_admin.NestedModelAdmin):
    model = Post
    inlines = [PostViewInline, LikeInline, CommentInline]

admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(PostView)
