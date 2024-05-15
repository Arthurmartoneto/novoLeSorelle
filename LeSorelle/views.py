from django.views.generic import TemplateView
from django.contrib.auth.views import redirect_to_login

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator, EmptyPage

from django.utils import timezone
from datetime import timedelta, date

from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from django.http import JsonResponse, HttpResponseRedirect

from .forms import ReservaForm, FoodForm

from .models import Food, Reserva, PratoAdicional

from django.db.models.signals import post_save
from django.db.models import Sum, F

import pdb
# Create your views here.


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['foods'] = Food.objects.all()  # Passe todos os alimentos para o contexto
        context['pratos'] = Food.objects.filter(status='ativo')
        initial_data = {}
        if self.request.user.is_authenticated:
            initial_data['name_completo'] = self.request.user.get_full_name()
            initial_data['email'] = self.request.user.email

            # Verifica se o usuário pertence ao grupo "Dashboard"
            user_is_in_dashboard_group = self.request.user.groups.filter(name='Dashboard').exists()
            context['user_is_in_dashboard_group'] = user_is_in_dashboard_group

        context['form'] = ReservaForm(initial=initial_data)
        return context
    
    def post(self, request, *args, **kwargs):
        form = ReservaForm(request.POST)
        if form.is_valid():
            telefone = request.POST.get('telefone')
            date = request.POST.get('date')
            hora = request.POST.get('hora')
            food_id = request.POST.get('food')
            peso = request.POST.get('peso')
            
            # Imprimir valores da reserva principal
            print(f"Telefone: {telefone}")
            print(f"Data: {date}")
            print(f"Hora: {hora}")
            print(f"ID do Alimento: {food_id}")
            print(f"Peso: {peso}")
            
            # Cria a reserva principal
            reserva_instance = Reserva.objects.create(usuario=request.user, telefone=telefone, date=date, hora=hora, food_id=food_id, peso=peso)
            
            num_pratos_adicionais = int(request.POST.get('num_pratos_adicionais'))
            
            for i in range(num_pratos_adicionais):
                nome_prato = request.POST.get('nome_prato_' + str(i))
                peso_prato = request.POST.get('peso_prato_' + str(i))
                
                # Imprimir valores dos pratos adicionais
                print(f"Nome do Prato Adicional {i}: {nome_prato}")
                print(f"Peso do Prato Adicional {i}: {peso_prato}")
                
                # Cria um prato adicional associado à reserva principal
                PratoAdicional.objects.create(reserva=reserva_instance, nome=nome_prato, peso=peso_prato)
            
            return redirect('pedidos')
        else:
            print(form.errors)
            return super().get(request, *args, **kwargs)



class dashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboards.html"
    login_url = '/login/'  # URL de login padrão, pode ser alterada conforme necessário

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Dashboard').exists():
            # Se o usuário não pertence ao grupo "Dashboard", redireciona para a página de login
            return redirect_to_login(request.get_full_path(), self.login_url)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservas'] = Reserva.objects.filter(date__gte=date.today()).order_by('date')
        context['reservas_modal'] = Reserva.objects.all()
        # Obtém os quatro últimos pratos para a página de dashboard
        foods_dashboard_reversed = reversed(Food.objects.all().order_by('-id')[:4])
        context['foods_dashboard'] = list(foods_dashboard_reversed)
        # Passa todos os pratos para o modal
        context['foods_modal'] = Food.objects.all()
        context['form'] = FoodForm()  # Inicialize o formulário
        
        # Calcular a média de vendas
        total_vendas = Reserva.objects.aggregate(total_vendas=Sum('food__valor'))
        total_reservas = Reserva.objects.count()
        if total_reservas > 0:
            media_vendas = total_vendas['total_vendas'] / total_reservas
        else:
            media_vendas = 0

        context['media_vendas'] = media_vendas

        # Adicionar contagem de vendas por dia
        vendas_por_dia = {}
        reservas_por_dia = Reserva.objects.values('date').annotate(total_vendas=Sum('food__valor'))
        for reserva in reservas_por_dia:
            data_reserva = reserva['date']
            vendas_por_dia[data_reserva] = reserva['total_vendas']
        # Se não houver reservas para um determinado dia, definimos a contagem de vendas como 0
        dias_sem_vendas = [day for day in (date.today() - timedelta(n) for n in range(7)) if day not in vendas_por_dia]
        for dia in dias_sem_vendas:
            vendas_por_dia[dia] = 0
        
        context['vendas_por_dia'] = vendas_por_dia

        # Calcular a soma total do valor das vendas
        soma_total_vendas = sum(vendas_por_dia.values())
        context['soma_total_vendas'] = soma_total_vendas
        

        # Calcular o preço total de cada reserva no modal
        soma_total_preco_modal = 0
        for reserva_modal in context['reservas_modal']:
            # Remover "g" do peso e converter para um número decimal
            peso_sem_g = reserva_modal.peso.replace('g', '')
            peso_decimal = Decimal(peso_sem_g) / 1000 if peso_sem_g.endswith('kg') else Decimal(peso_sem_g) / 1000
            # Calcular o preço total multiplicando o valor por kg do alimento pelo peso
            reserva_modal.preco_total = reserva_modal.food.valor * peso_decimal
            soma_total_preco_modal += reserva_modal.preco_total

        # Arredondar a soma total do preço para duas casas decimais
        soma_total_preco_modal = round(soma_total_preco_modal, 2)

        context['soma_total_preco_modal'] = soma_total_preco_modal
        
        
        # Calcular o preço total de cada reserva no modal
        soma_total_preco = 0
        for reserva in context['reservas']:
            # Remover "g" do peso e converter para um número decimal
            peso_sem_g = reserva.peso.replace('g', '')
            peso_decimal = Decimal(peso_sem_g) / 1000 if peso_sem_g.endswith('kg') else Decimal(peso_sem_g) / 1000
            # Calcular o preço total multiplicando o valor por kg do alimento pelo peso
            reserva.preco_total = reserva.food.valor * peso_decimal
            soma_total_preco += reserva.preco_total

        # Arredondar a soma total do preço para duas casas decimais
        soma_total_preco = round(soma_total_preco, 2)

        context['soma_total_preco'] = soma_total_preco
        
        # Calcula a diferença entre a soma total do preço e a meta de 500 reais por dia
        meta_diaria = 100  # Meta de 100 reais por dia
        total_vendido = soma_total_preco
        diferenca_meta = total_vendido - meta_diaria  # Calcula a diferença entre o total vendido e a meta

        context['diferenca_meta'] = diferenca_meta
        context['meta_diaria'] = meta_diaria  # Passa o valor da meta para o contexto
        
        data_atual = date.today()

        vendas_por_dia = Reserva.objects.filter(date=data_atual).count()
        meta_diaria_reservas = 10  # Meta de 10 reservas por dia
        diferenca_meta_reservas = vendas_por_dia - meta_diaria_reservas

        context['diferenca_meta_reservas'] = diferenca_meta_reservas
        context['meta_diaria_reservas'] = meta_diaria_reservas
        
        return context

    def post(self, request, *args, **kwargs):
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirecionar para a mesma página após a adição do prato
            return redirect('dashboard')
        else:
            # Se o formulário não for válido, recarregar a página com os erros do formulário
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)

def editar_prato(request, prato_id):
    if request.method == 'POST':
        nome = request.POST.get('editNome')
        descricao = request.POST.get('editDescricao')
        valor = request.POST.get('editValor')

        # Obtenha a imagem do formulário, se estiver presente
        imagem = request.FILES.get('editImagem')

        # Converte o valor para o formato correto
        try:
            valor_decimal = float(valor.replace(',', '.'))
        except ValueError:
            return JsonResponse({'error': 'O valor deve ser um número decimal válido.'}, status=400)

        prato = get_object_or_404(Food, id=prato_id)

        prato.name_food = nome
        prato.descricao = descricao
        prato.valor = valor_decimal  # Salva o valor convertido

        # Se houver uma nova imagem, salve-a
        if imagem:
            prato.img = imagem  # Atualize a imagem do prato

        prato.save()

        return JsonResponse({'message': 'Prato editado com sucesso!'})

    return JsonResponse({'error': 'Método não permitido'}, status=405)
    
def excluir_prato(request, prato_id):
    if request.method == 'POST':
        # Obtenha o objeto do prato a ser excluído
        prato = get_object_or_404(Food, id=prato_id)

        # Exclua o prato
        prato.delete()

        # Retorna uma resposta JSON indicando a exclusão bem-sucedida
        return JsonResponse({'success': True})

    # Se a solicitação não for POST, retorne uma resposta de erro
    return JsonResponse({'error': 'Método não permitido'}, status=405)

def inativar_prato(request, prato_id):
    prato = get_object_or_404(Food, id=prato_id)
    prato.status = 'inativo'
    prato.save()
    return JsonResponse({'message': 'Prato inativado com sucesso.'})

def ativar_prato(request, prato_id):
    prato = get_object_or_404(Food, id=prato_id)
    prato.status = 'ativo'
    prato.save()
    return JsonResponse({'message': 'Prato ativado com sucesso.'})


class tablesView(TemplateView):
    template_name = "tables/tables.html"
    
    
class pedidosView(TemplateView):
    template_name = "pedidos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Recupera as reservas do usuário atual
        reservas_usuario = Reserva.objects.filter(usuario=self.request.user)
        context['reservas_usuario'] = reservas_usuario
        
        # Calcular o preço total de cada reserva no modal
        soma_total_preco = 0
        for reserva in context['reservas_usuario']:
            # Remover "g" do peso e converter para um número decimal
            peso_sem_g = reserva.peso.replace('g', '')
            peso_decimal = Decimal(peso_sem_g) / 1000 if peso_sem_g.endswith('kg') else Decimal(peso_sem_g) / 1000
            # Calcular o preço total multiplicando o valor por kg do alimento pelo peso
            reserva.preco_total = reserva.food.valor * peso_decimal
            soma_total_preco += reserva.preco_total

        # Arredondar a soma total do preço para duas casas decimais
        soma_total_preco = round(soma_total_preco, 2)

        context['soma_total_preco'] = soma_total_preco
        
        return context

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
