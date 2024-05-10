from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import IndexView, dashboardView, registerView, loginView, tablesView, pedidosView, editar_prato
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('dashboard/', login_required(dashboardView.as_view()), name='dashboard'),
    path('dashboard/tables', login_required(tablesView.as_view()), name='tables'),
    path('pedidos', login_required(pedidosView.as_view()), name='pedidos'),
    path('register/', registerView.as_view(), name='register'),
    path('login/', loginView.as_view(), name='login'),
    path('editar_prato/<int:prato_id>/', editar_prato, name='editar_prato'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)