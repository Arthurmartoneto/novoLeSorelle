from django.views.generic import TemplateView
from django.contrib.auth.views import redirect_to_login

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect

from django.http import JsonResponse, HttpResponseRedirect

from .forms import ReservaForm

from .models import Food

from django.db.models.signals import post_save
# Create your views here.


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['foods'] = Food.objects.all()  # Passe todos os alimentos para o contexto
        initial_data = {}
        if self.request.user.is_authenticated:
            initial_data['name_completo'] = self.request.user.get_full_name()
            initial_data['email'] = self.request.user.email
        context['form'] = ReservaForm(initial=initial_data)
        return context
    
    def post(self, request, *args, **kwargs):
        form = ReservaForm(request.POST)
        if form.is_valid():
            
            hora = request.POST.get('hora')
            print("hora:", hora)  # Verifica o valor do campo de hora
            # Salva o formulário e retorna uma instância do modelo preenchida com os dados do formulário
            reserva_instance = form.save(commit=False)
            # O parâmetro commit=False evita que o objeto seja salvo no banco de dados imediatamente

            # Agora, podemos manipular a instância se necessário
            # Por exemplo, se quisermos adicionar algum dado extra antes de salvar
            reserva_instance.usuario = request.user  # Supondo que você tenha um campo "usuario" na sua reserva

            # Salva a instância no banco de dados
            reserva_instance.save()
            
            # Redireciona o usuário para a página inicial ou outra página, se desejado
            return HttpResponseRedirect('/')  # Substitua '/' pela URL desejada
        else:
            print(form.errors)
            # Se o formulário não for válido, renderize novamente a página com o formulário e os erros
            return super().get(request, *args, **kwargs)


class dashboardView(TemplateView):
    template_name = "dashboards.html"
    
    
class tablesView(TemplateView):
    template_name = "tables/tables.html"


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
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Verifica se a senha e a confirmação da senha são iguais
        if password != confirm_password:
            return render(request, self.template_name, {'error_message': 'As senhas não coincidem'})

        # Cria um novo usuário com os detalhes fornecidos
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)

        # Redireciona para a página de login após o registro
        return redirect('login')
