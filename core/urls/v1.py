from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from core.views import MyTokenObtainPairView
from newslettersapp.views import NewsletterViewSet
from tags.views import TagViewSet
from users.views import UserViewSet, activate_token, reset_password

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'newsletters', NewsletterViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('activate/<str:token>', activate_token),
    path('reset_password/<str:token>', reset_password),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
