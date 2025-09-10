from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="feed"),
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
    path("post/<int:post_id>/like/", views.like_post, name="like_post"),
    path("comment/<int:comment_id>/like/", views.like_comment, name="like_comment"),
    path("comment/<int:comment_id>/reply/", views.reply_comment, name="reply_comment"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("profiles/", views.profiles_list, name="profiles_list"),
    path("postar/", views.create_user_post, name="create_user_post"),
]
