from django.db import models
from django.contrib.auth.models import User

AVATAR_DEFAULT = "core/avatars/avatar1.png"


# ========================
# Perfis de usuário
# ========================
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.CharField(max_length=120, default=AVATAR_DEFAULT)
    bio = models.TextField(max_length=300, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


# ========================
# Posts oficiais
# ========================
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    summary = models.TextField(blank=True)
    content = models.TextField()
    cover = models.ImageField(upload_to="posts/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


# ========================
# Postagens da comunidade
# ========================
class UserPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")
    title = models.CharField(max_length=150)
    content = models.TextField()
    image = models.ImageField(upload_to="user_posts/", blank=True, null=True)
    embed_url = models.URLField("Link de vídeo (YouTube, Instagram, Facebook)", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    def is_youtube(self):
        return self.embed_url and ("youtube.com" in self.embed_url or "youtu.be" in self.embed_url)

    def is_instagram(self):
        return self.embed_url and "instagram.com" in self.embed_url

    def is_facebook(self):
        return self.embed_url and "facebook.com" in self.embed_url

    def youtube_embed(self):
        if not self.embed_url:
            return None
        url = self.embed_url

        # Se for link encurtado (youtu.be/ID)
        if "youtu.be/" in url:
            video_id = url.split("youtu.be/")[-1].split("?")[0]
            return f"https://www.youtube.com/embed/{video_id}"

        # Se for link normal (watch?v=ID)
        if "watch?v=" in url:
            video_id = url.split("watch?v=")[-1].split("&")[0]
            return f"https://www.youtube.com/embed/{video_id}"

        # Se já for embed
        if "embed/" in url:
            return url

        return url


# ========================
# Comentários e Curtidas (Posts oficiais)
# ========================
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")

    def __str__(self):
        return f"Comentário de {self.user.username} em {self.post.title}"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return f"{self.user.username} curtiu {self.post.title}"


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("comment", "user")

    def __str__(self):
        return f"{self.user.username} curtiu comentário {self.comment.id}"


# ========================
# Curtidas e Comentários (UserPost)
# ========================
class UserPostLike(models.Model):
    post = models.ForeignKey("UserPost", on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return f"{self.user.username} curtiu {self.post.title}"


class UserPostComment(models.Model):
    post = models.ForeignKey("UserPost", on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")

    def __str__(self):
        return f"Comentário de {self.user.username} em {self.post.title}"
