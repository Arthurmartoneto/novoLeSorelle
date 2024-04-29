from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .forms import ReservaForm

from django.db.models.signals import post_save
# Create your views here.


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def post(self, request, *args, **kwargs):
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

class dashboardView(TemplateView):
    template_name = "dashboards.html"
    

class loginView(TemplateView):
    template_name = "login/login.html"
    
    def post(self, request, *args, **kwargs):
            email = request.POST.get('username_or_email')  # Alterado para 'username_or_email'
            password = request.POST.get('password')
            remember_me = request.POST.get('remember_me') == 'on'

            # Autenticar usuário
            user = authenticate(request, username=email, password=password)  # Alterado para 'username'

            if user is not None:
                # Login bem-sucedido
                login(request, user)
                if remember_me:
                    # Defina um tempo de expiração mais longo para o login
                    request.session.set_expiry(604800)  # 1 semana em segundos
                return redirect('index')  # Redireciona para a página de dashboard após o login
            else:
                # Login falhou
                return render(request, self.template_name, {'error_message': 'E-mail ou senha inválidos'})  # Ajustado a mensagem de erro
    

class registerView(TemplateView):
    template_name = "login/register.html"

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name') 
        last_name = request.POST.get('last_name')    
        
        # Criar usuário com os dados fornecidos
        user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
        
        # Redirecionar para a página de login após o registro
        return redirect('login')