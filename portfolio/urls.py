from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='userView'),
    path('<str:username>/', views.DashboardView.as_view(), name='otherUserView')
]