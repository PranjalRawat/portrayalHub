from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()
router.register(r'profile/info', views.UserProfileViewSet, basename='userprofileInfo')
router.register(r'profile/image', views.UserProfileImageViewSet, basename='userprofileImage')
router.register(r'profile/resume', views.ResumeUploadViewSet, basename='userprofileResume')

router.register(r'social_platforms', views.SocialPlatformViewSet, basename='socialPlatforms')
router.register(r'education', views.EducationInfoViewSet, basename='educationInfo')
router.register(r'experience', views.ExperienceInfoViewSet, basename='experienceInfo')
router.register(r'certificates', views.CertificateInfoViewSet, basename='certificatesInfo')
router.register(r'skills', views.SkillsInfoViewSet, basename='skillsInfo')
router.register(r'projects', views.MajorProjectsInfoViewSet, basename='projectsInfo')

urlpatterns = [
    path('', include(router.urls)),

    path('user/<str:username>/profile/info/', views.OtherUserProfileView.as_view(), name='otherUserprofileInfo'),
    path('user/<str:username>/profile/image/', views.OtherUserProfileImageView.as_view(), name='otherUserprofileImage'),
    path('user/<str:username>/profile/resume/', views.OtherResumeUploadView.as_view(), name='otherUserprofileResume'),

    path('user/<str:username>/social_platforms/', views.OtherSocialPlatformView.as_view(), name='otherSocialPlatforms'),
    path('user/<str:username>/education/', views.OtherEducationInfoView.as_view(), name='otherEducationInfo'),
    path('user/<str:username>/experience/', views.OtherExperienceInfoView.as_view(), name='otherExperienceInfo'),
    path('user/<str:username>/certificates/', views.OtherCertificateInfoView.as_view(), name='otherCertificatesInfo'),
    path('user/<str:username>/skills/', views.OtherSkillsInfoView.as_view(), name='otherSkillsInfo'),
    path('user/<str:username>/projects/', views.OtherMajorProjectsInfoView.as_view(), name='otherProjectsInfo'),


    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
