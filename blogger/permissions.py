from rest_framework import permissions

from blog.models.blog import Post
from user.models.user import User


def check_post_owner(post: Post, user: User) -> bool:
    """
    checks the authenticated user for the post
    """

    return post.author == user