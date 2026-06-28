from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('messages', views.TelegramMessageViewSet, basename='telegram-message')

urlpatterns = [
    path('check-user/', views.check_user.as_view(), name = 'check_user'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('hello/', views.HelloWorldView.as_view(), name='hello_world'),
    path('', include(router.urls)),
]
