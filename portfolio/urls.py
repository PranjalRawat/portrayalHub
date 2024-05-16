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
]

# Add a catch-all pattern for page not found errors
urlpatterns += [
    path('<path:path>/', views.PageNotFoundView.as_view(), name='page_not_found'),
]
