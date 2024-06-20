from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """
    Represents a blog post.

    Attributes:
        title (str): The title of the blog post.
        author (User): The author of the blog post.
        content (str): The content of the blog post.
        created_at (datetime): The date and time when the blog post was created.
        updated_at (datetime): The date and time when the blog post was last updated.
    """

    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    """
    Represents a comment on a blog post.

    Attributes:
        author (User): The user who wrote the comment.
        post (Post): The blog post that the comment belongs to.
        content (str): The content of the comment.
        created_at (datetime): The date and time when the comment was created.
    """

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
