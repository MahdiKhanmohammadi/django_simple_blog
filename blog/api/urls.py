from rest_framework.routers import SimpleRouter
from .views import CategoryModelViewSet, PostModelViewSet


router = SimpleRouter()
router.register("category", CategoryModelViewSet, basename='api_category')
router.register("post", PostModelViewSet, basename='api_post')

urlpatterns = router.urls
