from turtle import title

from django.utils.text import slugify
from rest_framework import serializers

from blog.models.blog import Comment, Post


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
    
    def update(self, instance, validated_data):

        #  if a user updates slug we'll use the updated slug---.  if they dont, we use the initial slug, and save to db---
        # if they delete slug enntirely, we'll generate a slug from the title---.
        #  when they update slug and that slug is already in the database, we add a number to the slug. 

        if validated_data.get('slug') is None:
            return super().update(instance, validated_data)
        
        elif not validated_data.get('slug'):
            title = validated_data.get('title', instance.title)
            new_slug = slugify(title)
        else:
            new_slug = validated_data['slug']

        slug = new_slug
        counter = 2

        while Post.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
            slug = f"{new_slug}-{counter}"
            counter += 1

        validated_data['slug'] = slug

        return super().update(instance, validated_data)
    

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    post = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = "__all__"

        read_only_fields = ["post", "author", "created_at"]

class SearchSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, required=False, allow_blank=True)
    content = serializers.CharField(max_length=100, required=False, allow_blank=True)
    slug = serializers.CharField(max_length=100, required=False, allow_blank=True)
    date = serializers.DateTimeField(required=False)
    author = serializers.IntegerField(required=False)
    
class SearchPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

        read_only_fields = ["title", "content", "slug", "created_at", "updated_at", "author"]