from django.db import models
from django.contrib.auth.models import User

# ========================
# Perfis de usuário
# ========================
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", default="avatars/default.png")
    bio = models.TextField(max_length=300, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


# ========================
# Posts oficiais (publicados pelo admin)
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

    # 🚨 novo campo
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    # helpers para identificar tipo de embed
    def is_youtube(self):
        return self.embed_url and ("youtube.com" in self.embed_url or "youtu.be" in self.embed_url)

    def is_instagram(self):
        return self.embed_url and "instagram.com" in self.embed_url

    def is_facebook(self):
        return self.embed_url and "facebook.com" in self.embed_url

    def youtube_embed(self):
        """Transforma link do YouTube em embed se necessário"""
        if not self.embed_url:
            return None
        if "watch?v=" in self.embed_url:
            return self.embed_url.replace("watch?v=", "embed/")
        return self.embed_url


# ========================
# Curtidas e comentários (já existiam)
# ========================
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

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
