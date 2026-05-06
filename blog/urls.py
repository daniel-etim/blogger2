from django.urls import path

from blog.views.blog import create_post, list_post, read_post


urlpatterns = [
    path("list/", list_post, name="post_list"),
    path("create/", create_post, name="post_create"),
    path("read/<int:pk>/", read_post, name="post_read"),
]