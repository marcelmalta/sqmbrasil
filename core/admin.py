from django.contrib import admin
from .models import Post, Comment, Like, Profile, UserPost


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


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "updated_at")
    search_fields = ("user__username", "user__email")


@admin.register(UserPost)
class UserPostAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created_at", "is_approved")
    list_filter = ("is_approved", "created_at")
    search_fields = ("title", "content", "user__username")
    actions = ["aprovar_posts", "reprovar_posts"]

    @admin.action(description="Aprovar posts selecionados")
    def aprovar_posts(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description="Reprovar posts selecionados")
    def reprovar_posts(self, request, queryset):
        queryset.update(is_approved=False)
