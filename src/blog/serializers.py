from rest_framework import serializers
from .models import Category, Post, Comment, Like, PostView


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "post_count"
        )


class CommentSerializer(serializers.ModelSerializer):

    commenter = serializers.StringRelatedField()
    post = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = (
            "commenter",
            "post",
            "time_stamp",
            "content",
        )


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    author = serializers.StringRelatedField()
    category = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = (
            "title",
            "content",
            "image_URL",
            "category",
            "publish_date",
            "update_date",
            "author",
            "author_avatar",
            "status",
            "is_liked",
            "slug",
            "comment_count",
            "like_count",
            "view_count",
            "comments"
        )

        # extra_kwargs = {
        #     "publish_date": {"read_only": True},
        #     "author": {"read_only": True},
        #     "is_liked": {"read_only": True},
        #     "slug": {"read_only": True},
        #     "comment_count": {"read_only": True},
        #     "like_count": {"read_only": True},
        #     "view_count": {"read_only": True},
        #     "comments": {"read_only": True},
        # }


class PostEditSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    category = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = (
            "title",
            "content",
            "image_URL",
            "category",
            "update_date",
            "author_avatar",
            "status",
        )


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            "user",
            "post",
        )


class PostViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostView
        fields = (
            "user",
            "post",
            "time_stamp"
        )


