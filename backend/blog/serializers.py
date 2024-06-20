from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"

    def get_created_at(self, obj):
        return obj.created_at.strftime("%d/%m/%Y")

    def get_updated_at(self, obj):
        return obj.created_at.strftime("%d/%m/%Y")


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("post",)

    def get_created_at(self, obj):
        return obj.created_at.strftime("%d/%m/%Y")
