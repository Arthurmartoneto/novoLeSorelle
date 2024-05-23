from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import IndexView, dashboardView, registerView, loginView, tablesView, reservasView, finalizadasView, editar_prato, excluir_prato, inativar_prato, ativar_prato, cancelar_reserva, marcar_em_preparo, marcar_pronto, marcar_finalizado, get_notifications, clear_notifications
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', IndexView.as_view(), name='index'),
    
    path('dashboard/', login_required(dashboardView.as_view()), name='dashboard'),
    path('dashboard/tables', login_required(tablesView.as_view()), name='tables'),
    path('dashboard/finalizadas', login_required(finalizadasView.as_view()), name='finalizadas'),
    
    path('minhasreservas', login_required(reservasView.as_view()), name='minhasreservas'),
    
    path('register/', registerView.as_view(), name='register'),
    path('login/', loginView.as_view(), name='login'),
    
    
    path('excluir_prato/<int:prato_id>/', excluir_prato, name='excluir_prato'),
    path('editar_prato/<int:prato_id>/', editar_prato, name='editar_prato'),
    path('inativar_prato/<int:prato_id>/', inativar_prato, name='inativar_prato'),
    path('ativar_prato/<int:prato_id>/', ativar_prato, name='ativar_prato'),
    path('cancelar_reserva/<int:reserva_id>/', cancelar_reserva, name='cancelar_reserva'),
    path('marcar_em_preparo/<int:reserva_id>/', marcar_em_preparo, name='marcar_em_preparo'),
    path('marcar_pronto/<int:reserva_id>/', marcar_pronto, name='marcar_pronto'),
    path('marcar_finalizado/<int:reserva_id>/', marcar_finalizado, name='marcar_finalizado'),
    path('get-notifications/', get_notifications, name='get_notifications'),
    path('clear-notifications/', clear_notifications, name='clear_notifications'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)