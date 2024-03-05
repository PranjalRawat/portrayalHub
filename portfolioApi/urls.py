from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'info', views.UserProfileViewSet, basename='userprofileInfo')
router.register(r'image', views.UserProfileImageViewSet, basename='userprofileImage')
router.register(r'resume', views.ResumeUploadViewSet, basename='userprofileResume')

urlpatterns = [
    path('profile/', include(router.urls)),
    path('social-profiles/', views.SocialPlatformView.as_view()),
    path('social-profiles/<int:pk>', views.SocialPlatformDetailView.as_view()),
    path('education-info/', views.EducationInfoView.as_view()),
    path('education-info/<int:pk>', views.EducationInfoDetailView.as_view()),
]
