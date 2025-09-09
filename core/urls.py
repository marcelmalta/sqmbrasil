from django.urls import path
from . import views

urlpatterns = [
    # Feed principal (posts oficiais + comunidade aprovada)
    path("", views.home, name="feed"),

    # Detalhe de post oficial
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),

    # Ação de curtir/descurtir post oficial (POST)
    path("post/<int:post_id>/like/", views.like_post, name="like_post"),

    # Perfis
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("profiles/", views.profiles_list, name="profiles_list"),

    # Postagens da comunidade
    path("postar/", views.create_user_post, name="create_user_post"),
]
