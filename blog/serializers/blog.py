from rest_framework import serializers

from blog.models.blog import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    class Meta:
        model = Post
        fields = "__all__"

        read_only_fields = ['created_at', 'updated_at', 'author']