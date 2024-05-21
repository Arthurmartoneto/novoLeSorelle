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
from datetime import timedelta, date, datetime

from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from django.http import JsonResponse, HttpResponseRedirect

from .forms import ReservaForm, FoodForm

from .models import Food, Reserva, PratoAdicional

from django.db.models.signals import post_save
from django.db.models import Sum, F

from itertools import groupby

import pdb
# Create your views here.


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['foods'] = Food.objects.filter(status='ativo')  # Passe todos os alimentos para o contexto
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
            telefone = form.cleaned_data['telefone']
            date = form.cleaned_data['date']
            hora = form.cleaned_data['hora']
            food_id = form.cleaned_data['food']
            peso = form.cleaned_data['peso']
            
            # Imprimir valores da reserva principal
            print(f"Telefone: {telefone}")
            print(f"Data: {date}")
            print(f"Hora: {hora}")
            print(f"ID do Alimento: {food_id}")
            print(f"Peso: {peso}")
            
            # Cria a reserva principal
            reserva_instance = form.save(commit=False)
            reserva_instance.usuario = request.user
            reserva_instance.save()
            
            # Salva os pratos adicionais
            pratos_adicionais = request.POST.getlist('nome_prato')
            pesos_pratos_adicionais = request.POST.getlist('peso_prato')

            for i in range(len(pratos_adicionais)):
                nome_prato_id = pratos_adicionais[i]  # ID do alimento
                peso_prato = pesos_pratos_adicionais[i]
                
                # Recupera o objeto Food a partir do ID
                nome_prato = Food.objects.get(pk=nome_prato_id)
                
                # Recupera o valor do prato adicional
                valor_prato = nome_prato.valor
                
                # Imprimir valores dos pratos adicionais
                print(f"ID Prato Adicional {i}: {nome_prato_id}")
                print(f"Peso do Prato Adicional {i}: {peso_prato}")
                print(f"Valor do Prato Adicional {i}: {valor_prato}")
                
                # Cria um prato adicional associado à reserva principal
                PratoAdicional.objects.create(reserva=reserva_instance, food=nome_prato, peso=peso_prato, valor=valor_prato)

            
            return redirect('pedidos')
        else:
            print(form.errors)
            return super().get(request, *args, **kwargs)


class dashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboards.html"
    login_url = '/login/'  

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Dashboard').exists():
            return redirect_to_login(request.get_full_path(), self.login_url)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Adicionar os pratos adicionais ao contexto
        context['foods_modal'] = Food.objects.all()
        
        # Filtrar as reservas para hoje e ordená-las por data
        reservas_abertas = Reserva.objects.filter(date__gte=date.today(), status__in=['pendente', 'em_preparo', 'pronto']).order_by('date')
        reservas_finalizadas = Reserva.objects.filter(status='finalizado').order_by('date')
        
        # Adicionar as reservas ao contexto
        context['reservas_abertas'] = reservas_abertas
        context['reservas_finalizadas'] = reservas_finalizadas
        
        # Calcular o preço total de cada reserva
        for reserva in reservas_abertas:
            # Calcular o preço total do prato principal
            peso_principal = Decimal(reserva.peso.replace('kg', '').replace('g', '').strip()) / 1000 if reserva.peso else 0
            reserva.preco_principal = reserva.food.valor * peso_principal

            # Calcular o preço total dos pratos adicionais, se houver
            preco_adicionais = sum(prato_adicional.food.valor * Decimal(prato_adicional.peso.replace('kg', '').replace('g', '').strip()) / 1000 for prato_adicional in reserva.pratos_adicionais_reserva.all())
            reserva.preco_adicionais = preco_adicionais

            # Calcular o preço total da reserva
            reserva.preco_total = reserva.preco_principal + reserva.preco_adicionais
        
        # Calcular o preço total de cada reserva finalizada
        for reserva_finalizada in reservas_finalizadas:
            peso_principal = Decimal(reserva_finalizada.peso.replace('kg', '').replace('g', '').strip()) / 1000 if reserva_finalizada.peso else 0
            reserva_finalizada.preco_principal = reserva_finalizada.food.valor * peso_principal
            preco_adicionais = sum(prato_adicional.food.valor * Decimal(prato_adicional.peso.replace('kg', '').replace('g', '').strip()) / 1000 for prato_adicional in reserva_finalizada.pratos_adicionais_reserva.all())
            reserva_finalizada.preco_adicionais = preco_adicionais
            reserva_finalizada.preco_total = reserva_finalizada.preco_principal + reserva_finalizada.preco_adicionais

        # Calcular a soma total do valor das reservas
        context['soma_total_preco'] = sum(reserva.preco_total for reserva in reservas_abertas) + sum(reserva_finalizada.preco_total for reserva_finalizada in reservas_finalizadas)

        # Calcular a média de vendas
        total_vendas = Reserva.objects.aggregate(total_vendas=Sum('food__valor'))
        total_reservas = Reserva.objects.count()
        context['media_vendas'] = total_vendas['total_vendas'] / total_reservas if total_reservas > 0 else 0

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
        context['soma_total_vendas'] = sum(vendas_por_dia.values())

        # Calcular a diferença entre a soma total do preço e a meta de 500 reais por dia
        meta_diaria = 100  # Meta de 100 reais por dia
        context['diferenca_meta'] = context['soma_total_preco'] - meta_diaria
        context['meta_diaria'] = meta_diaria
        
        data_atual = date.today()
        vendas_por_dia_atual = Reserva.objects.filter(date=data_atual).count()
        context['diferenca_meta_reservas'] = vendas_por_dia_atual - 10  # Meta de 10 reservas por dia
        context['meta_diaria_reservas'] = 10  # Passa o valor da meta de reservas para o contexto

        # Adicionar os pratos adicionais ao contexto
        context['foods_dashboard'] = Food.objects.all()

        # Adicionar o formulário de adição de pratos ao contexto
        context['form'] = FoodForm()

        return context

    def post(self, request, *args, **kwargs):
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)
        

@login_required        
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

@login_required    
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

@login_required
def inativar_prato(request, prato_id):
    prato = get_object_or_404(Food, id=prato_id)
    prato.status = 'inativo'
    prato.save()
    return JsonResponse({'message': 'Prato inativado com sucesso.'})

@login_required
def ativar_prato(request, prato_id):
    prato = get_object_or_404(Food, id=prato_id)
    prato.status = 'ativo'
    prato.save()
    return JsonResponse({'message': 'Prato ativado com sucesso.'})

@login_required
def marcar_em_preparo(request, reserva_id):
    if request.method == 'POST':
        reserva = get_object_or_404(Reserva, id=reserva_id)
        reserva.status = 'em_preparo'
        reserva.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def marcar_pronto(request, reserva_id):
    if request.method == 'POST':
        reserva = get_object_or_404(Reserva, id=reserva_id)
        reserva.status = 'pronto'
        reserva.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def marcar_finalizado(request, reserva_id):
    if request.method == 'POST':
        reserva = get_object_or_404(Reserva, id=reserva_id)
        reserva.status = 'finalizado'
        reserva.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


class tablesView(TemplateView):
    template_name = "tables/tables.html"
    

class pedidosView(TemplateView):
    template_name = "pedidos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Recupera as reservas do usuário atual
        reservas_usuario = Reserva.objects.filter(usuario=self.request.user)

        # Defina a data atual
        data_atual = datetime.now().date()

        # Separe as reservas em reservas antes e depois da data atual
        reservas_passadas = reservas_usuario.filter(date__lt=data_atual)
        reservas_futuras = reservas_usuario.filter(date__gte=data_atual)

        # Adicione as reservas passadas e futuras ao contexto
        context['reservas_passadas'] = reservas_passadas
        context['reservas_futuras'] = reservas_futuras
        
        # Definir função para calcular o preço total de um prato
        def calcular_preco_convertido(valor, peso):
            peso_sem_kg = peso.replace('kg', '')
            peso_sem_g = peso.replace('g', '')

            if peso.endswith('kg'):
                peso_decimal = Decimal(peso_sem_kg)
            else:
                peso_decimal = Decimal(peso_sem_g) / 1000

            return valor * peso_decimal

        # Calcular o preço convertido individual de cada prato e adicionar ao contexto para reservas passadas
        for reserva in reservas_passadas:
            # Calcular o preço convertido do prato principal
            reserva.preco_principal = calcular_preco_convertido(reserva.food.valor, reserva.peso)
            
            # Calcular o preço convertido dos pratos adicionais, se houver
            reserva.preco_adicionais = sum(calcular_preco_convertido(prato_adicional.valor, prato_adicional.peso) for prato_adicional in reserva.pratos_adicionais_reserva.all())

            # Somar o preço do prato principal com o preço dos pratos adicionais
            reserva.preco_total = reserva.preco_principal + reserva.preco_adicionais

        # Calcular o preço convertido individual de cada prato e adicionar ao contexto para reservas futuras
        for reserva in reservas_futuras:
            # Calcular o preço convertido do prato principal
            reserva.preco_principal = calcular_preco_convertido(reserva.food.valor, reserva.peso)
            
            # Calcular o preço convertido dos pratos adicionais, se houver
            reserva.preco_adicionais = sum(calcular_preco_convertido(prato_adicional.valor, prato_adicional.peso) for prato_adicional in reserva.pratos_adicionais_reserva.all())

            # Somar o preço do prato principal com o preço dos pratos adicionais
            reserva.preco_total = reserva.preco_principal + reserva.preco_adicionais

        return context

@login_required
def cancelar_reserva(request, reserva_id):
    if request.method == 'POST':
        reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)
        reserva.status = 'cancelado'
        reserva.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

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
