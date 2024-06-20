from rest_framework import routers
from .views import CommentViewSet, PostViewSet

router = routers.DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(r'posts/(?P<post_pk>[^/.]+)/comments', CommentViewSet, basename='post-comments')
router.register(r'comments', CommentViewSet)


urlpatterns = router.urls
