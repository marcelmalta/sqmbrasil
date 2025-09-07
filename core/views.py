from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment, Like

def home(request):
    posts = Post.objects.filter(published=True).only(
        "id","title","slug","summary","cover","created_at"
    )
    return render(request, "core/home.html", {"posts": posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)

    # Enviar comentário
    if request.method == "POST" and "comment" in request.POST:
        if request.user.is_authenticated:
            content = request.POST.get("comment")
            if content.strip():
                Comment.objects.create(post=post, user=request.user, content=content)
                messages.success(request, "Comentário publicado!")
                return redirect("post_detail", slug=slug)
        else:
            messages.error(request, "Você precisa estar logado para comentar.")

    comments = post.comments.select_related("user")
    user_liked = False
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(post=post, user=request.user).exists()

    return render(request, "core/post_detail.html", {
        "post": post,
        "comments": comments,
        "user_liked": user_liked,
    })

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id, published=True)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        messages.info(request, "Você retirou seu like.")
    else:
        messages.success(request, "Você curtiu este post!")
    return redirect("post_detail", slug=post.slug)
