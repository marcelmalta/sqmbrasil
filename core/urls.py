from django.urls import path
from . import views

urlpatterns = [
    # Feed principal (posts oficiais + comunidade)
    path("", views.home, name="feed"),

    # Detalhes de post oficial
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),

    # Perfis
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("profiles/", views.profiles_list, name="profiles_list"),

    # Postagens da comunidade
    path("postar/", views.create_user_post, name="create_user_post"),
]
