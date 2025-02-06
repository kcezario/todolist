from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.tasks import TaskViewSet
from .views.auth import register, login, logout, me, users, user_detail, create_user

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('auth/register/', register, name='register'),
    path('auth/login/', login, name='login'),
    path('auth/logout/', logout, name='logout'),
    path('auth/me/', me, name='me'),
    path('auth/users/', users, name='users'),
    path('auth/users/<int:id>/', user_detail, name='user_detail'),
    path('auth/create-user/', create_user, name='create_user'),
    path('', include(router.urls)),
]
