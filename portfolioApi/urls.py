from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


profile = DefaultRouter()
profile.register(r'info', views.UserProfileViewSet, basename='userprofileInfo')
profile.register(r'image', views.UserProfileImageViewSet, basename='userprofileImage')
profile.register(r'resume', views.ResumeUploadViewSet, basename='userprofileResume')

education = DefaultRouter()
education.register(r'info', views.EducationInfoViewSet, basename='educationInfo')

urlpatterns = [
    path('profile/', include(profile.urls)),
    path('education/', include(education.urls)),
    path('social-profiles/', views.SocialPlatformView.as_view()),
    path('social-profiles/<int:pk>', views.SocialPlatformDetailView.as_view()),
]
