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

certificates = DefaultRouter()
certificates.register(r'info', views.CertificateInfoViewSet, basename='certificatesInfo')

skills = DefaultRouter()
skills.register(r'info', views.SkillsInfoViewSet, basename='skillsInfo')

projects = DefaultRouter()
projects.register(r'info', views.MajorProjectsInfoViewSet, basename='projectsInfo')

urlpatterns = [
    path('profile/', include(profile.urls)),
    path('education/', include(education.urls)),
    path('experience/', include(experience.urls)),
    path('certificates/', include(certificates.urls)),
    path('skills/', include(skills.urls)),
    path('projects/', include(projects.urls)),
    path('social-profiles/', views.SocialPlatformView.as_view()),
    path('social-profiles/<int:pk>', views.SocialPlatformDetailView.as_view()),
]
