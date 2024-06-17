from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Comment


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for testing
        test_user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Create a post for testing
        Post.objects.create(
            title="Test Post", author=test_user, content="This is a test post"
        )

    def test_title(self):
        post = Post.objects.get(id=1)
        title = post.title
        self.assertEqual(title, "Test Post")

    def test_author(self):
        post = Post.objects.get(id=1)
        author = post.author
        self.assertEqual(author.username, "testuser")

    def test_content(self):
        post = Post.objects.get(id=1)
        content = post.content
        self.assertEqual(content, "This is a test post")

    def test_created_at_auto_now_add(self):
        post = Post.objects.get(id=1)
        created_at = post.created_at
        self.assertIsNotNone(created_at)

    def test_updated_at_auto_now(self):
        post = Post.objects.get(id=1)
        updated_at = post.updated_at
        self.assertIsNotNone(updated_at)


class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for testing
        test_user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Create a post for testing
        cls.test_post = Post.objects.create(
            title="Test Post", author=test_user, content="This is a test post"
        )

        # Create a comment for testing
        Comment.objects.create(
            post=cls.test_post, author=test_user, content="This is a test comment"
        )

    def test_post_relationship(self):
        comment = Comment.objects.get(id=1)
        post_from_comment = comment.post
        expected_post = self.test_post

        self.assertEqual(post_from_comment, expected_post)

    def test_author(self):
        comment = Comment.objects.get(id=1)
        author = comment.author
        self.assertEqual(author.username, "testuser")

    def test_content(self):
        comment = Comment.objects.get(id=1)
        content = comment.content
        self.assertEqual(content, "This is a test comment")

    def test_created_at_auto_now_add(self):
        comment = Comment.objects.get(id=1)
        created_at = comment.created_at
        self.assertIsNotNone(created_at)
