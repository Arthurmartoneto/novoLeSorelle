from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
# Create your views here.

class IndexView(TemplateView):
    template_name = "index.html"

class dashboardView(TemplateView):
    template_name = "dashboards.html"

class loginView(TemplateView):
    template_name = "login/login.html"

    def post(self, request, *args, **kwargs):
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me') == 'on'

        # Autenticar usuário
        user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            # Login bem-sucedido
            login(request, user)
            if remember_me:
                # Defina um tempo de expiração mais longo para o login
                request.session.set_expiry(604800)  # 1 week in seconds
            return redirect('index')  # Redirecione para a página de dashboard após o login
        else:
            # Login falhou
            return render(request, self.template_name, {'error_message': 'Invalid username or password'})
    

class registerView(TemplateView):
    template_name = "login/register.html"

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Criar usuário
        user = User.objects.create_user(username, email, password)
        # Faça o que precisar com o usuário criado
        # Por exemplo, redirecione para a página de login
        return redirect('login')  # Supondo que 'login' seja o nome da URL para a página de login