from django.urls import path

from blog.views.blog import create_post, delete_post, list_post, read_post, update_post, delete_post, comment_post


urlpatterns = [
    path("list/", list_post, name="post_list"),
    path("create/", create_post, name="post_create"),
    path("read/<int:pk>/", read_post, name="post_read"),
    path("update/<int:pk>/", update_post, name="post_update"),
    path("delete/<int:pk>/", delete_post, name="post_delete"),
    path("comment/<int:pk>/", comment_post, name="post_comment"),
]