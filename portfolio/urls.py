from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='userView'),
    path('user/<str:username>/', views.DashboardView.as_view(), name='otherUserView'),
    path('login/', views.LogInView.as_view(), name='loginView'),
    path('logout/', views.LogOutView.as_view(), name='logoutView'),
]

# Add a catch-all pattern for page not found errors
urlpatterns += [
    path('<path:path>/', views.PageNotFoundView.as_view(), name='page_not_found'),
]
