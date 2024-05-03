from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import IndexView, dashboardView, registerView, loginView, tablesView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('dashboard/', login_required(dashboardView.as_view()), name='dashboard'),
    path('dashboard/tables', login_required(tablesView.as_view()), name='tables'),
    path('register/', registerView.as_view(), name='register'),
    path('login/', loginView.as_view(), name='login'),
]