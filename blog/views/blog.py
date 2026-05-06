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