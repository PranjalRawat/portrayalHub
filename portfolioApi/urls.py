from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()
router.register(r'profile/info', views.UserProfileViewSet, basename='userprofileInfo')
router.register(r'profile/image', views.UserProfileImageViewSet, basename='userprofileImage')
router.register(r'profile/resume', views.ResumeUploadViewSet, basename='userprofileResume')

router.register(r'education', views.EducationInfoViewSet, basename='educationInfo')
router.register(r'experience', views.ExperienceInfoViewSet, basename='experienceInfo')
router.register(r'certificates', views.CertificateInfoViewSet, basename='certificatesInfo')
router.register(r'skills', views.SkillsInfoViewSet, basename='skillsInfo')
router.register(r'projects', views.MajorProjectsInfoViewSet, basename='projectsInfo')

urlpatterns = [
    path('', include(router.urls)),
    path('social-profiles/', views.SocialPlatformView.as_view()),
    path('social-profiles/<int:pk>', views.SocialPlatformDetailView.as_view()),

    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
