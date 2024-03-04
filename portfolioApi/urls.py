from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'info', views.UserProfileViewSet, basename='userprofile')
router.register(r'image', views.UserProfileImageViewSet, basename='userprofileImage')

urlpatterns = [
    path('profile/', include(router.urls)),
    path('social-profiles/', views.SocialPlatformView.as_view()),
    path('social-profiles/<int:pk>', views.SocialPlatformDetailView.as_view()),
]
