from django.db import models
from django.utils.text import slugify

class Post(models.Model):
    title = models.CharField("Título", max_length=160)
    slug = models.SlugField("Slug", max_length=180, unique=True, blank=True)
    summary = models.CharField("Resumo (subtítulo)", max_length=240, blank=True)
    content = models.TextField("Conteúdo")
    cover = models.ImageField("Capa (opcional)", upload_to="posts/", blank=True, null=True)
    published = models.BooleanField("Publicado", default=True)

    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            i = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)
