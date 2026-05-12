from django.urls import path

from blog.views.blog import create_comment, create_post, delete_comment, delete_post, list_post, read_post, update_post, delete_post


urlpatterns = [
    path("list/", list_post, name="post_list"),
    path("create/", create_post, name="post_create"),
    path("read/<int:pk>/", read_post, name="post_read"),
    path("update/<int:pk>/", update_post, name="post_update"),
    path("delete/<int:pk>/", delete_post, name="post_delete"),
    path("create/<int:pk>/comment", create_comment, name="comment_create"),
    path("delete/<int:pk>/comment", delete_comment, name="comment_delete"),
]