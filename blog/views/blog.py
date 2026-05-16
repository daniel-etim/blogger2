from datetime import date

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from blog.models.blog import Comment, Post
from blog.serializers.blog import CommentSerializer, PostReadSerializer, PostSerializer, SearchPostSerializer, SearchSerializer


@api_view(["GET"])
def list_post(request: Request):
    posts = Post.objects.all().order_by("-created_at")

    serializer = PostSerializer(posts, many=True)

    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_post(request: Request):
    serializer = PostSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    serializer.save(author=request.user)

    return Response(data=serializer.data, status=status.HTTP_201_CREATED)

@api_view(["GET"])
@permission_classes([IsAuthenticatedOrReadOnly])
def read_post(request: Request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(data={"error": "Post Not Found"}, status=status.HTTP_404_NOT_FOUND)
    
    comments = Comment.objects.filter(post_id=pk)

    serializer = PostReadSerializer(post)
    comments_serializer = CommentSerializer(comments, many=True)

    return Response(data={"post": serializer.data, "comments": comments_serializer.data}, status=status.HTTP_200_OK)

@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_post(request: Request, pk:int):
    try:
        post :Post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(data={"error": "Post Not Found"}, status=status.HTTP_404_NOT_FOUND)

    if post.author != request.user and not request.user.is_staff:
        return Response(data={"error": "You're not authorized to edit this post"}, status=status.HTTP_401_UNAUTHORIZED)
    
    serializer = PostSerializer(post, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)

    serializer.save()

    return Response(data={"message": "successfully updated", "data": serializer.data}, status=status.HTTP_205_RESET_CONTENT)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_post(request: Request, pk: int):
    try:
        post = Post.objects.get(pk=pk)
    except  Post.DoesNotExist:
        return Response(data={"error": "Post Not Found"}, status=status.HTTP_404_NOT_FOUND)

    if post.author != request.user and not request.user.is_staff:
        return Response(data={"error": "You're not authorized to do this"}, status=status.HTTP_403_FORBIDDEN)
    
    post.delete()

    return Response(data={"message": "Post Deleted"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_comment(request: Request, pk: int):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(data={"error": "Post Not Found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CommentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    serializer.save(author=request.user, post=post)

    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_comment(request: Request, pk: int):
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return Response(data={"error": "Post Not Found"}, status=status.HTTP_404_NOT_FOUND)
    
    if comment.author != request.user:
        return Response(data={"error": "You're not authorized to do this"}, status=status.HTTP_401_UNAUTHORIZED)
    
    comment.delete()

    return Response(data={"message": "Deleted"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def search(request: Request):
    search = SearchSerializer(data=request.data)
    search.is_valid(raise_exception=True)

    clean_data = search.validated_data

    if not any(clean_data):
        return Response(data={"error": "please provide at least one search parameter"}, status=status.HTTP_400_BAD_REQUEST)

    posts = Post.objects.all()

    if clean_data.get("title"):
        posts = posts.filter(title__icontains=clean_data["title"])
    if clean_data.get("content"):
        posts = posts.filter(content__icontains=clean_data["content"])
    if clean_data.get("slug"):
        posts = posts.filter(slug__icontains=clean_data["slug"])
    if clean_data.get("date"):
        posts = posts.filter(created_at__date=clean_data["date"].date())
    if clean_data.get("author"):
        posts = posts.filter(author_id=clean_data["author"])


    if not posts.exists():
        return Response(data={"search": "NO CONTENT"}, status=status.HTTP_404_NOT_FOUND)

    serializer = SearchPostSerializer(posts, many=True)

    return Response(data={"search": serializer.data}, status=status.HTTP_200_OK)