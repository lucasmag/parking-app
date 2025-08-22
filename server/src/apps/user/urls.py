from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from apps.user.views import UserViewSet

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='user')
urlpatterns = [
    path('', include(router.urls)),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
