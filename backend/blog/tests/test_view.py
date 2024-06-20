from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from ..models import Post, Comment
from ..serializers import PostSerializer, CommentSerializer


class PostViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.post = Post.objects.create(
            title="Test Post", content="This is a test post", author=self.user
        )
        self.comment = Comment.objects.create(
            content="This is a test comment", author=self.user, post=self.post
        )

    def test_create_post(self):
        """
        Test that a new post can be created.
        """
        url = reverse("post-list")
        data = {
            "title": "New Post",
            "content": "This is a new post",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(
            Post.objects.get(title="New Post").content, "This is a new post"
        )
        self.assertEqual(Post.objects.get(title="New Post").author, self.user)

    def test_create_post_with_empty_title(self):
        """
        Test that a new post cannot be created with an empty title.
        """
        url = reverse("post-list")
        data = {
            "title": "",
            "content": "This is a new post",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.json()["details"])
        self.assertEqual(
            response.json()["details"]["title"][0], "This field may not be blank."
        )

    def test_create_post_with_no_title(self):
        """
        Test that a new post cannot be created without a title.
        """
        url = reverse("post-list")
        data = {
            "content": "This is a new post",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.json()["details"])
        self.assertEqual(
            response.json()["details"]["title"][0], "This field is required."
        )

    def test_create_post_with_whitespace_title(self):
        """
        Test that a new post cannot be created with a whitespace title.
        """
        url = reverse("post-list")
        data = {
            "title": "   ",
            "content": "This is a new post",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.json()["details"])
        self.assertEqual(
            response.json()["details"]["title"][0], "This field may not be blank."
        )

    def test_create_post_with_empty_content(self):
        """
        Test that a new post cannot be created with empty content.
        """
        url = reverse("post-list")
        data = {
            "title": "New Post",
            "content": "",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("content", response.json()["details"])
        self.assertEqual(
            response.json()["details"]["content"][0], "This field may not be blank."
        )

    def test_create_post_with_no_content(self):
        """
        Test that a new post cannot be created without content.
        """
        url = reverse("post-list")
        data = {
            "title": "New Post",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("content", response.json()["details"])
        self.assertEqual(
            response.json()["details"]["content"][0], "This field is required."
        )

    def test_retrieve_post(self):
        """
        Test that a specific post can be retrieved.
        """
        url = reverse("post-detail", args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.post.title)
        self.assertEqual(response.data["content"], self.post.content)
        self.assertEqual(response.data["author"], self.user.username)
        self.assertEqual(len(response.data["comments"]), 1)
        self.assertEqual(response.data["comments"][0]["content"], self.comment.content)
        self.assertEqual(response.data["comments"][0]["author"], self.user.username)

    def test_update_post(self):
        """
        Test that a post can be updated.
        """
        url = reverse("post-detail", args=[self.post.id])
        data = {
            "title": "Updated Post",
            "content": "This is an updated post",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.get(id=self.post.id).title, "Updated Post")
        self.assertEqual(
            Post.objects.get(id=self.post.id).content, "This is an updated post"
        )

    def test_delete_post(self):
        """
        Test that a post can be deleted.
        """
        url = reverse("post-detail", args=[self.post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_most_commented_posts(self):
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")

        # Create posts
        self.post1 = Post.objects.create(
            title="Post 1", content="Content 1", author=self.user1
        )
        self.post2 = Post.objects.create(
            title="Post 2", content="Content 2", author=self.user1
        )
        self.post3 = Post.objects.create(
            title="Post 3", content="Content 3", author=self.user1
        )
        self.post4 = Post.objects.create(
            title="Post 4", content="Content 4", author=self.user2
        )
        self.post5 = Post.objects.create(
            title="Post 5", content="Content 5", author=self.user2
        )
        self.post6 = Post.objects.create(
            title="Post 6", content="Content 6", author=self.user2
        )

        # Create comments
        for i in range(5):
            Comment.objects.create(
                post=self.post1, author=self.user2, content="Comment {}".format(i)
            )

        for i in range(3):
            Comment.objects.create(
                post=self.post2, author=self.user1, content="Comment {}".format(i)
            )

        for i in range(1):
            Comment.objects.create(
                post=self.post3, author=self.user2, content="Comment {}".format(i)
            )

        Comment.objects.create(post=self.post4, author=self.user1, content="Comment 0")

        url = reverse("post-most-commented")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

        # Check the order of the posts (most comments first)
        self.assertEqual(response.data[0]["id"], self.post1.id)
        self.assertEqual(response.data[1]["id"], self.post2.id)
        self.assertEqual(
            response.data[2]["id"], self.post.id
        )  # self.post has 1 comment
        self.assertEqual(response.data[3]["id"], self.post3.id)
        self.assertEqual(response.data[4]["id"], self.post4.id)


class CommentViewSetTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")

        self.post = Post.objects.create(
            title="Post", content="Post content", author=self.user1
        )

        self.comment = Comment.objects.create(
            post=self.post, author=self.user2, content="Comment content"
        )

        # Set up URLs
        self.list_create_url = reverse(
            "post-comments-list", kwargs={"post_pk": self.post.pk}
        )
        self.detail_url = reverse(
            "post-comments-detail",
            kwargs={"post_pk": self.post.pk, "pk": self.comment.pk},
        )
        self.generic_comment_detail_url = reverse(
            "comment-detail", kwargs={"pk": self.comment.pk}
        )

    def test_create_comment(self):
        self.client.login(username="user2", password="password")
        data = {"content": "New comment content"}
        response = self.client.post(self.list_create_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["content"], "New comment content")
        self.assertEqual(response.data["author"], "user2")
        self.assertEqual(int(response.data["post"]), self.post.pk)

    def test_create_comment_with_empty_content(self):
        self.client.login(username="user2", password="password")
        data = {"content": ""}
        response = self.client.post(self.list_create_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("content", response.json()["details"])
        self.assertEqual(
            response.json()["details"]["content"][0], "This field may not be blank."
        )

    def test_create_comment_with_no_content(self):
        self.client.login(username="user2", password="password")
        response = self.client.post(self.list_create_url, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("content", response.json()["details"])
        self.assertEqual(
            response.json()["details"]["content"][0], "This field is required."
        )

    def test_create_comment_with_whitespace_content(self):
        self.client.login(username="user2", password="password")
        data = {"content": "   "}
        response = self.client.post(self.list_create_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("content", response.json()["details"])
        self.assertEqual(
            response.json()["details"]["content"][0], "This field may not be blank."
        )

    def test_list_comments(self):
        response = self.client.get(self.list_create_url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["content"], "Comment content")
        self.assertEqual(response.data[0]["author"], "user2")

    def test_retrieve_comment(self):
        response = self.client.get(self.detail_url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "Comment content")
        self.assertEqual(response.data["author"], "user2")

    def test_update_comment(self):
        self.client.login(username="user2", password="password")
        data = {"content": "Updated comment content"}
        response = self.client.put(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "Updated comment content")

    def test_partial_update_comment(self):
        self.client.login(username="user2", password="password")
        data = {"content": "Partially updated comment content"}
        response = self.client.patch(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "Partially updated comment content")

    def test_delete_comment(self):
        self.client.login(username="user2", password="password")
        response = self.client.delete(self.detail_url, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_cannot_update_other_users_comment(self):
        self.client.login(username="user1", password="password")
        data = {"content": "Updated by another user"}
        response = self.client.put(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_delete_other_users_comment(self):
        self.client.login(username="user1", password="password")
        response = self.client.delete(self.detail_url, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
