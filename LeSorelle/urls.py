from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import IndexView, dashboardView, registerView, loginView

urlpatterns = [
    path('', login_required(IndexView.as_view()), name='index'),
    path('dashboard/', login_required(dashboardView.as_view()), name='dashboard'),
    path('register/', registerView.as_view(), name='register'),
    path('login/', loginView.as_view(), name='login'),
]