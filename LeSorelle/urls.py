from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import IndexView, dashboardView, registerView, loginView, tablesView, reservasView, finalizadasView, redefinicao, blogView
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', IndexView.as_view(), name='index'),
    
    path('dashboard/', login_required(dashboardView.as_view()), name='dashboard'),
    path('dashboard/tables', login_required(tablesView.as_view()), name='tables'),
    path('dashboard/finalizadas', login_required(finalizadasView.as_view()), name='finalizadas'),
    path('dashboard/blog', login_required(blogView.as_view()), name='blog'),
    
    path('minhasreservas', login_required(reservasView.as_view()), name='minhasreservas'),
    
    path('register/', registerView.as_view(), name='register'),
    path('redefinicao/', redefinicao.as_view(), name='redefinicao'),
    path('login/', loginView.as_view(), name='login'),    
    
    path('excluir_prato/<int:prato_id>/', views.excluir_prato, name='excluir_prato'),
    path('editar_prato/<int:prato_id>/', views.editar_prato, name='editar_prato'),
    path('inativar_prato/<int:prato_id>/', views.inativar_prato, name='inativar_prato'),
    path('ativar_prato/<int:prato_id>/', views.ativar_prato, name='ativar_prato'),
    path('cancelar_reserva/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),
    path('marcar_em_preparo/<int:reserva_id>/', views.marcar_em_preparo, name='marcar_em_preparo'),
    path('marcar_pronto/<int:reserva_id>/', views.marcar_pronto, name='marcar_pronto'),
    path('marcar_finalizado/<int:reserva_id>/', views.marcar_finalizado, name='marcar_finalizado'),
    path('get-notifications/', views.get_notifications, name='get_notifications'),
    path('clear-notifications/', views.clear_notifications, name='clear_notifications'),
    
    path('excluir_blog/<int:id>/', views.excluir_blog, name='excluir_blog'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)