from rest_framework.viewsets import ModelViewSet
from .models import Post, Comment
from .serializers import CommentSerializer, PostSerializer
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from django.db.models import Count


class PostViewSet(ModelViewSet):
    """
    A viewset for handling CRUD operations on the Post model.

    Attributes:
        queryset (QuerySet): The queryset of all Post objects.
        serializer_class (Serializer): The serializer class for Post objects.
        permission_classes (list): The list of permission classes for PostViewSet.

    Methods:
        perform_create(serializer): Performs additional actions when creating a new Post object.
        retrieve(request, *args, **kwargs): Retrieves a specific Post object and its associated comments.
        most_commented(request): Retrieves the top 5 posts with the most comments.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        comments_serializer = CommentSerializer(instance.comments.all(), many=True)
        data = serializer.data
        data["comments"] = comments_serializer.data
        return Response(data)

    @action(detail=False, methods=["get"], url_path="most-commented")
    def most_commented(self, request):
        """
        Retrieve the top 5 posts with the most comments.

        Returns:
            A Response object containing the serialized data of the top posts.
        """
        top_posts = Post.objects.annotate(comment_count=Count("comments")).order_by(
            "-comment_count"
        )
        if top_posts.count() > 4:
            top_posts = top_posts[:5]

        serializer = self.get_serializer(top_posts, many=True)
        return Response(serializer.data)


class CommentViewSet(ModelViewSet):
    """
    A viewset for handling comments on blog posts.

    This viewset provides CRUD operations for comments, including creating,
    retrieving, updating, and deleting comments.

    Attributes:
        queryset (QuerySet): The queryset of all comments.
        serializer_class (Serializer): The serializer class for comments.
        permission_classes (list): The list of permission classes for comments.

    Methods:
        perform_create: Performs additional actions when creating a comment.
        get_queryset: Retrieves the queryset of comments based on the post.
        create: Creates a new comment for a specific post.

    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        """
        Performs additional actions when creating a comment.

        This method is called when a new comment is being created. It sets the
        author of the comment to the current user and associates the comment
        with the corresponding post.

        Args:
            serializer (Serializer): The serializer instance for the comment.

        """
        post_id = self.kwargs["post_pk"]
        serializer.save(author=self.request.user, post_id=post_id)

    def get_queryset(self):
        """
        Retrieves the queryset of comments based on the post.

        This method is called when retrieving the comments for a specific post.
        It filters the comments based on the post ID.

        Returns:
            QuerySet: The queryset of comments for the post.

        """
        if "post_pk" in self.kwargs:
            post_id = self.kwargs["post_pk"]
            return Comment.objects.filter(post_id=post_id)
        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        """
        Creates a new comment for a specific post.

        This method is called when creating a new comment for a specific post.
        It associates the comment with the corresponding post and returns the
        created comment.

        Args:
            request (Request): The request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The response containing the created comment.

        """
        post_id = self.kwargs["post_pk"]
        request.data["post"] = post_id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
