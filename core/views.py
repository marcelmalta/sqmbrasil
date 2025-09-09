from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.timezone import now

from .models import Post, Comment, Like, Profile, UserPost
from .forms import ProfileForm, UserPostForm


# =========================
# Feed principal (posts oficiais + posts de usuários aprovados)
# =========================
def home(request):
    posts = Post.objects.filter(published=True).order_by("-created_at")
    user_posts = (
        UserPost.objects.filter(is_approved=True)
        .select_related("user")
        .order_by("-created_at")
    )

    combined = []
    for p in posts:
        combined.append({"type": "oficial", "obj": p})
    for up in user_posts:
        combined.append({"type": "usuario", "obj": up})

    combined_posts = sorted(combined, key=lambda x: x["obj"].created_at, reverse=True)
    return render(request, "core/home.html", {"combined_posts": combined_posts})


# =========================
# Detalhe de post oficial + comentários
# =========================
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)

    # Publicar comentário (se enviado)
    if request.method == "POST" and request.user.is_authenticated:
        content = (request.POST.get("comment") or "").strip()
        if content:
            Comment.objects.create(post=post, user=request.user, content=content)
            messages.success(request, "Comentário publicado!")
            return redirect("post_detail", slug=post.slug)

    comments = Comment.objects.filter(post=post).order_by("-created_at")

    # Variáveis esperadas pelo template
    user_liked = (
        request.user.is_authenticated
        and Like.objects.filter(post=post, user=request.user).exists()
    )
    likes_count = post.likes.count()

    return render(
        request,
        "core/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "user_liked": user_liked,
            "likes_count": likes_count,
        },
    )


# =========================
# Curtidas em posts oficiais (somente POST)
# =========================
@login_required
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, published=True)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        # Já existia like -> descurte
        like.delete()
    return redirect("post_detail", slug=post.slug)


# =========================
# Perfis de usuário
# =========================
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    user_posts = UserPost.objects.filter(user=profile_user).order_by("-created_at")
    return render(
        request,
        "core/profile.html",
        {"profile_user": profile_user, "user_posts": user_posts},
    )


@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(
            request.POST, request.FILES, instance=profile, user=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect("profile", username=request.user.username)
    else:
        form = ProfileForm(instance=profile, user=request.user)
    return render(request, "core/edit_profile.html", {"form": form})


def profiles_list(request):
    profiles = Profile.objects.select_related("user").all()
    return render(request, "core/profiles_list.html", {"profiles": profiles})


# =========================
# Postagens da comunidade (UserPost)
# =========================
@login_required
def create_user_post(request):
    # Regra: 1 post por dia
    last_post = (
        UserPost.objects.filter(user=request.user).order_by("-created_at").first()
    )
    if last_post and last_post.created_at.date() == now().date():
        messages.error(request, "Você só pode postar uma vez por dia.")
        return redirect("profile", username=request.user.username)

    if request.method == "POST":
        form = UserPostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.is_approved = False  # precisa aprovação do admin
            new_post.save()
            messages.success(
                request,
                "Sua postagem foi enviada com sucesso. Ela ficará visível no seu perfil, "
                "mas só aparecerá na página inicial depois que for aprovada por um administrador.",
            )
            return redirect("profile", username=request.user.username)
    else:
        form = UserPostForm()

    return render(request, "core/user_post_form.html", {"form": form})
