from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/', views.DashboardView.as_view(), name='home'),
    # Define more web app routes here as needed
]