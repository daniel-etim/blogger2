from django.utils.text import slugify
from rest_framework import serializers

from blog.models.blog import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    slug = serializers.SlugField(required=False, allow_blank=True)
    
    class Meta:
        model = Post
        fields = "__all__"

        read_only_fields = ['created_at', 'updated_at', 'author']

    def create(self, validated_data):
        if not validated_data.get('slug'):
            slug = slugify(validated_data['title'])
        else:
            slug = validated_data['slug']
            
        original_slug = slug

        counter = 2

        while Post.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"

            counter += 1
        
        validated_data['slug'] = slug

        return super().create(validated_data)