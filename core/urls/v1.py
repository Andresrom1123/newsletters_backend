from django.urls import path, include
from rest_framework import routers

from newslettersapp.views import NewsletterViewSet
from tags.views import TagViewSet
from users.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'newsletters', NewsletterViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls))
]
