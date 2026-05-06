from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from blog.models.blog import Post
from blog.serializers.blog import PostSerializer


@api_view(["GET"])
def list_post(request: Request):
    blogs = Post.objects.all().order_by("-created_at")

    serializer = PostSerializer(blogs, many=True)

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
    post = Post.objects.get(pk=pk)
    
    serializer = PostSerializer(post)

    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_post(request: Request, pk:int):
    try:
        post :Post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(data={"error": "Post Not Found"}, status=status.HTTP_404_NOT_FOUND)

    if post.author != request.user:
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

    if post.author != request.user:
        return Response(data={"error": "You're not authorized to do this. Go call the owner!"}, status=status.HTTP_403_FORBIDDEN)
    
    post.delete()

    return Response(data={"message": "Post Deleted"}, status=status.HTTP_204_NO_CONTENT)