from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views.tasks import TaskViewSet
from .views.auth import register, me

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('auth/register/', register, name='register'),
    path('auth/me/', me, name='me'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('', include(router.urls))
]
