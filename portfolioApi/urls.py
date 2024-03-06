from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


profile = DefaultRouter()
profile.register(r'info', views.UserProfileViewSet, basename='userprofileInfo')
profile.register(r'image', views.UserProfileImageViewSet, basename='userprofileImage')
profile.register(r'resume', views.ResumeUploadViewSet, basename='userprofileResume')

education = DefaultRouter()
education.register(r'info', views.EducationInfoViewSet, basename='educationInfo')

experience = DefaultRouter()
experience.register(r'info', views.ExperienceInfoViewSet, basename='experienceInfo')

certificate = DefaultRouter()
certificate.register(r'info', views.CertificateInfoViewSet, basename='certificateInfo')

skill = DefaultRouter()
skill.register(r'info', views.SkillsInfoViewSet, basename='skillInfo')

urlpatterns = [
    path('profile/', include(profile.urls)),
    path('education/', include(education.urls)),
    path('experience/', include(experience.urls)),
    path('certificate/', include(certificate.urls)),
    path('skill/', include(skill.urls)),
    path('social-profiles/', views.SocialPlatformView.as_view()),
    path('social-profiles/<int:pk>', views.SocialPlatformDetailView.as_view()),
]
