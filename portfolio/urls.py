from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='userView'),
    path('user/<str:username>/', views.DashboardView.as_view(), name='otherUserView')
]

# Add a catch-all pattern for page not found errors
urlpatterns += [
    path('<path:path>/', views.PageNotFoundView.as_view(), name='page_not_found'),
]
