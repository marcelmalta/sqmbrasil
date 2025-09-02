from django.shortcuts import render, get_object_or_404
from .models import Post

def home(request):
    posts = Post.objects.filter(published=True).only("id","title","slug","summary","cover","created_at")
    return render(request, "core/home.html", {"posts": posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    return render(request, "core/post_detail.html", {"post": post})
