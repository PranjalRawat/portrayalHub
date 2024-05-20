from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='userView'),
    path('user/<str:username>/', views.DashboardView.as_view(), name='otherUserView'),
    path('profile/', views.ProfileEditView.as_view(), name='profileEditView'),
    path('login/', views.LogInView.as_view(), name='loginView'),
    path('logout/', views.LogOutView.as_view(), name='logoutView'),

    path('profile/info/update/<int:pk>/', views.UpdateProfileView.as_view(), name='updateProfileView'),
    path('profile/image/update/<int:pk>/', views.UpdateProfileImageView.as_view(), name='updateProfileImageView'),
    path('profile/resume/update/<int:pk>/', views.UpdateResumeUploadView.as_view(), name='updateResumeUploadView'),

    path('profile/social_platforms/create/', views.CreateSocialPlatformView.as_view(), name='createSocialPlatformView'),
    path('profile/social_platforms/delete/<int:pk>', views.DeleteSocialPlatformView.as_view(), name='deleteSocialPlatformView'),
    path('profile/social_platforms/update/<int:pk>/', views.UpdateSocialPlatformView.as_view(), name='updateSocialPlatformView'),

    path('profile/education/create/', views.CreateEducationInfoView.as_view(), name='createEducationInfoView'),
    path('profile/education/delete/<int:pk>', views.DeleteEducationInfoView.as_view(), name='deleteEducationInfoView'),
    path('profile/education/update/<int:pk>/', views.UpdateEducationInfoView.as_view(), name='updateEducationInfoView'),

    path('profile/experience/create/', views.CreateExperienceInfoView.as_view(), name='createExperienceInfoView'),
    path('profile/experience/delete/<int:pk>', views.DeleteExperienceInfoView.as_view(), name='deleteExperienceInfoView'),
    path('profile/experience/update/<int:pk>/', views.UpdateExperienceInfoView.as_view(), name='updateExperienceInfoView'),

    path('profile/skill/create/', views.CreateSkillsInfoView.as_view(), name='createSkillsInfoView'),
    path('profile/skill/delete/<int:pk>', views.DeleteSkillsInfoView.as_view(), name='deleteSkillsInfoView'),
    path('profile/skill/update/<int:pk>/', views.UpdateSkillsInfoView.as_view(), name='updateSkillsInfoView'),
]

# Add a catch-all pattern for page not found errors
urlpatterns += [
    path('<path:path>/', views.PageNotFoundView.as_view(), name='page_not_found'),
]
