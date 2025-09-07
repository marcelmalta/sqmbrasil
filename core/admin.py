from django.contrib import admin
from .models import Post, Comment, Like

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "published", "created_at", "likes_count_display")
    list_filter = ("published", "created_at")
    search_fields = ("title", "summary", "content")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"

    def likes_count_display(self, obj):
        return obj.likes.count()
    likes_count_display.short_description = "Curtidas"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "created_at")
    search_fields = ("content", "user__username")
    list_filter = ("created_at",)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "post__title")
