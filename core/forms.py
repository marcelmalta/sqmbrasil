from django import forms
from urllib.parse import urlparse
from django.contrib.auth.models import User

from .models import Profile, UserPost, AVATAR_DEFAULT

DEFAULT_AVATARS = [
    "core/avatars/avatar1.png",
    "core/avatars/avatar2.png",
    "core/avatars/avatar3.png",
    "core/avatars/avatar4.png",
    "core/avatars/avatar5.png",
    "core/avatars/avatar6.png",
    "core/avatars/avatar7.png",
    "core/avatars/avatar8.png",
    "core/avatars/avatar9.png",
]


class ProfileForm(forms.ModelForm):
    username = forms.CharField(
        max_length=30,
        required=True,
        label="Nome de usuário",
        widget=forms.TextInput(attrs={
            "placeholder": "Escolha seu nome de usuário",
            "class": "w-full border rounded-md p-3"
        })
    )

    avatar_choice = forms.ChoiceField(
        label="Escolha seu avatar",
        required=True,
        choices=[(p, p.split("/")[-1].replace(".png", "").capitalize()) for p in DEFAULT_AVATARS],
        widget=forms.RadioSelect
    )

    class Meta:
        model = Profile
        fields = ["bio", "avatar"]  # avatar é setado via avatar_choice no save()
        widgets = {
            "bio": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Conte brevemente sua experiência com SQM...",
                "class": "w-full border rounded-md p-3"
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields["username"].initial = self.user.username
        current = self.instance.avatar or AVATAR_DEFAULT
        self.fields["avatar_choice"].initial = current

    def clean_username(self):
        username = self.cleaned_data["username"]

        import re
        if not re.match(r'^[a-zA-Z0-9._-]+$', username):
            raise forms.ValidationError(
                "O nome de usuário só pode conter letras, números, ponto (.), underline (_) e hífen (-)."
            )
        if len(username) < 3 or len(username) > 20:
            raise forms.ValidationError("O nome de usuário deve ter entre 3 e 20 caracteres.")

        qs = User.objects.filter(username__iexact=username)
        if self.user:
            qs = qs.exclude(pk=self.user.pk)
        if qs.exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")
        return username

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            self.user.username = self.cleaned_data["username"]
            self.user.save()
        profile.avatar = self.cleaned_data.get("avatar_choice") or AVATAR_DEFAULT
        if commit:
            profile.save()
        return profile


class UserPostForm(forms.ModelForm):
    class Meta:
        model = UserPost
        fields = ["title", "content", "image", "embed_url"]
        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Título do seu relato/artigo",
                "class": "w-full border rounded-md p-3"
            }),
            "content": forms.Textarea(attrs={
                "rows": 8,
                "placeholder": "Escreva seu relato, artigo, depoimento ou notícia sobre SQM...",
                "class": "w-full border rounded-md p-3"
            }),
            "embed_url": forms.URLInput(attrs={
                "placeholder": "Cole um link de vídeo (YouTube, Instagram ou Facebook) — opcional",
                "class": "w-full border rounded-md p-3"
            }),
        }

    def clean_embed_url(self):
        url = self.cleaned_data.get("embed_url")
        if not url:
            return url
        netloc = urlparse(url).netloc.lower()
        allowed = (
            "youtube.com", "youtu.be",
            "instagram.com", "www.instagram.com",
            "facebook.com", "www.facebook.com"
        )
        if not any(d in netloc for d in allowed):
            raise forms.ValidationError("Apenas links de YouTube, Instagram ou Facebook são permitidos.")
        return url
