from django.views.generic import TemplateView
from django.contrib.auth.views import redirect_to_login

from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils.translation import gettext_lazy as _

from datetime import timedelta, date, datetime
from django.utils import timezone

from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404

from django.http import JsonResponse, HttpResponseRedirect

from .forms import ReservaForm, FoodForm, BlogForm

from .models import Food, Reserva, PratoAdicional, Notification, Blog

from django.db.models.signals import post_save
from django.db.models import Sum

from django.contrib import messages

# Create your views here.


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['foods'] = Food.objects.filter(status='ativo')  # Passe todos os alimentos para o contexto
        context['pratos'] = Food.objects.filter(status='ativo')
        blogs = Blog.objects.all()
        context['blogs'] = blogs
        context['no_posts'] = not blogs.exists()
        initial_data = {}
        if self.request.user.is_authenticated:
            initial_data['name_completo'] = self.request.user.get_full_name()
            initial_data['email'] = self.request.user.email

            # Verifica se o usuário pertence ao grupo "Dashboard"
            user_is_in_dashboard_group = self.request.user.groups.filter(name='Dashboard').exists()
            context['user_is_in_dashboard_group'] = user_is_in_dashboard_group

        context['form'] = ReservaForm(initial=initial_data)
        context['modo_choices'] = dict(Reserva.MODO_CHOICES)  # Adicione esta linha
        return context
    
    def post(self, request, *args, **kwargs):
        form = ReservaForm(request.POST)
        if form.is_valid():
            telefone = form.cleaned_data['telefone']
            date = form.cleaned_data['date']
            hora = form.cleaned_data['hora']
            food_id = form.cleaned_data['food']
            peso = form.cleaned_data['peso']
            modo = form.cleaned_data['modo']  # Captura o modo selecionado no formulário

            reserva_instance = form.save(commit=False)
            reserva_instance.usuario = request.user
            reserva_instance.modo = modo  # Salva o modo na reserva principal
            reserva_instance.save()

            pratos_adicionais = request.POST.getlist('nome_prato')
            pesos_pratos_adicionais = request.POST.getlist('peso_prato')
            modos_pratos_adicionais = request.POST.getlist('modo')  # Ajuste o nome do campo para capturar os modos dos pratos adicionais

            for i in range(len(pratos_adicionais)):
                nome_prato_id = pratos_adicionais[i]
                peso_prato = pesos_pratos_adicionais[i]
                modo_prato = modos_pratos_adicionais[i]  # Captura o modo do prato adicional

                nome_prato = Food.objects.get(pk=nome_prato_id)
                valor_prato = nome_prato.valor
                                
                # Cria um prato adicional associado à reserva principal
                PratoAdicional.objects.create(reserva=reserva_instance, food=nome_prato, peso=peso_prato, modo=modo_prato, valor=valor_prato)
                
                # Verifica se a reserva atende aos critérios para gerar uma notificação
            if reserva_instance.status == 'pendente':
                # Cria a mensagem da notificação
                notification_message = f"{reserva_instance.food.name_food} está {reserva_instance.status}."

                # Salva a notificação no banco de dados
                Notification.objects.create(subject='Reserva Pendente', message=notification_message)

            messages.success(request, 'Sua reserva foi realizada com sucesso!')

            return redirect('minhasreservas')
        else:
            print(form.errors)
            return super().get(request, *args, **kwargs)
        

@login_required
def get_notifications(request):
    notifications = Notification.objects.all()

    notifications_data = []
    for notification in notifications:
        notifications_data.append({
            'subject': notification.subject,
            'message': notification.message,
            'created_at': timezone.localtime(notification.created_at).strftime("%d/%m/%Y %H:%M"),  # Formatando o created_at
            # Adicione mais campos, se necessário
        })

    return JsonResponse({'notifications': notifications_data})

@login_required
def clear_notifications(request):
    try:
        # Limpar todas as notificações do banco de dados
        Notification.objects.all().delete()
        # Responder com uma mensagem de sucesso
        return JsonResponse({'message': 'Notificações limpas com sucesso.'})
    except Exception as e:
        # Se ocorrer um erro, responder com uma mensagem de erro
        return JsonResponse({'error': str(e)}, status=500)
    
    
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
        data_atual = timezone.now().date()  # Usando timezone.now() para obter a data e hora atuais
        reservas_abertas = Reserva.objects.filter(date__gte=data_atual, status__in=['pendente', 'em_preparo', 'pronto']).order_by('date')
        reservas_finalizadas = Reserva.objects.filter(status='finalizado', date__gte=data_atual).order_by('date')
        reservas_canceladas = Reserva.objects.filter(status='cancelado', date__gte=data_atual).order_by('date')
        
        # Adicionar as reservas ao contexto
        context['reservas_abertas'] = reservas_abertas
        context['reservas_finalizadas'] = reservas_finalizadas
        context['reservas_canceladas'] = reservas_canceladas
        
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
        reservas_por_dia = Reserva.objects.filter(date__gte=data_atual).values('date').annotate(total_vendas=Sum('food__valor'))
        for reserva in reservas_por_dia:
            data_reserva = reserva['date']
            vendas_por_dia[data_reserva] = reserva['total_vendas']
        
        # Se não houver reservas para um determinado dia, definimos a contagem de vendas como 0
        dias_sem_vendas = [day for day in (data_atual - timedelta(n) for n in range(7)) if day not in vendas_por_dia]
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
        
        context['blog_form'] = BlogForm()

        return context

    def post(self, request, *args, **kwargs):
        if 'food_submit' in request.POST:  # Se o formulário de Food foi submetido
            food_form = FoodForm(request.POST, request.FILES)
            if food_form.is_valid():
                food_form.save()
                return redirect('dashboard')
            else:
                context = self.get_context_data()
                context['form'] = food_form
                return render(request, self.template_name, context)
        elif 'blog_submit' in request.POST:  # Se o formulário de Blog foi submetido
            blog_form = BlogForm(request.POST, request.FILES)
            if blog_form.is_valid():
                blog = blog_form.save(commit=False)
                blog.usuario = request.user
                blog.save()
                return redirect('blog')
            else:
                context = self.get_context_data()
                context['blog_form'] = blog_form
                return render(request, self.template_name, context)
        
        # Se nenhum formulário foi submetido ou nenhum dos ramos anteriores foi acionado,
        # renderize a página com o contexto padrão
        return render(request, self.template_name, self.get_context_data())
        

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


class blogView(TemplateView):
    template_name = "blog.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Dashboard').exists():
            return redirect_to_login(request.get_full_path(), self.login_url)
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs'] = Blog.objects.all()  # Recupera todos os objetos do modelo Blog
        context['blog_form'] = BlogForm()  # Adiciona o formulário de adição de blog ao contexto
        context['form'] = FoodForm()  # Adiciona o formulário de adição de prato ao contexto
        return context
    
    def post(self, request, *args, **kwargs):
        if 'food_submit' in request.POST:  # Se o formulário de Food foi submetido
            food_form = FoodForm(request.POST, request.FILES)
            if food_form.is_valid():
                food_form.save()
                return redirect('dashboard')
            else:
                context = self.get_context_data()
                context['form'] = food_form
                return render(request, self.template_name, context)
        elif 'blog_submit' in request.POST:  # Se o formulário de Blog foi submetido
            blog_form = BlogForm(request.POST, request.FILES)
            if blog_form.is_valid():
                blog = blog_form.save(commit=False)
                blog.usuario = request.user
                blog.save()
                return redirect('blog')
            else:
                context = self.get_context_data()
                context['blog_form'] = blog_form
                return render(request, self.template_name, context)
        
        # Se nenhum formulário foi submetido ou nenhum dos ramos anteriores foi acionado,
        # renderize a página com o contexto padrão
        return render(request, self.template_name, self.get_context_data())
    
@login_required  
def excluir_blog(request, id):
    blog = get_object_or_404(Blog, pk=id)

    if request.method == "POST":
        try:
            blog.delete()
            print("Blog excluído com sucesso!")
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            print("Erro ao excluir o blog:", e)
            return JsonResponse({'status': 'error'}, status=500)
    else:
        print("Método de requisição inválido.")
        return JsonResponse({'status': 'fail'}, status=400)
    

class finalizadasView(TemplateView):
    template_name = "finalizadas.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Dashboard').exists():
            return redirect_to_login(request.get_full_path(), self.login_url)
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Adicionar os pratos adicionais ao contexto
        context['foods_modal'] = Food.objects.all()
        
        # Filtrar as reservas finalizadas e ordená-las por data
        reservas_finalizadas = Reserva.objects.filter(status='finalizado').order_by('date')
        context['reservas_finalizadas'] = reservas_finalizadas
        
        # Calcular o preço total de cada reserva finalizada
        valor_total = Decimal(0)
        for reserva_finalizada in reservas_finalizadas:
            if reserva_finalizada.peso:
                peso_principal_str = reserva_finalizada.peso.replace('kg', '').replace('g', '').strip()
                peso_principal = Decimal(peso_principal_str) / (1000 if 'g' in reserva_finalizada.peso else 1)
            else:
                peso_principal = Decimal(0)

            reserva_finalizada.preco_principal = reserva_finalizada.food.valor * peso_principal

            preco_adicionais = Decimal(0)
            for prato_adicional in reserva_finalizada.pratos_adicionais_reserva.all():
                peso_adicional_str = prato_adicional.peso.replace('kg', '').replace('g', '').strip()
                peso_adicional = Decimal(peso_adicional_str) / (1000 if 'g' in prato_adicional.peso else 1)
                preco_adicionais += prato_adicional.food.valor * peso_adicional

            reserva_finalizada.preco_adicionais = preco_adicionais
            reserva_finalizada.preco_total = reserva_finalizada.preco_principal + preco_adicionais

            valor_total += reserva_finalizada.preco_total

        # Adicionar a soma total ao contexto
        context['valor_total'] = valor_total
        
        # Adicionar o número total de reservas finalizadas ao contexto
        total_reservas_finalizadas = reservas_finalizadas.count()
        context['total_reservas'] = total_reservas_finalizadas

        return context

    
class tablesView(TemplateView):
    template_name = "tables/tables.html"

    def dispatch(self, request, *args, **kwargs):
            if not request.user.groups.filter(name='Dashboard').exists():
                return redirect_to_login(request.get_full_path(), self.login_url)
            return super().dispatch(request, *args, **kwargs)

    
    
class reservasView(TemplateView):
    template_name = "minhasreservas.html"

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
        
        # Adicionar modos dos pratos adicionais ao contexto para reservas passadas
        for reserva in reservas_passadas:
            pratos_adicionais = reserva.pratos_adicionais_reserva.all()
            modos_pratos_adicionais = [(prato.food.name_food, prato.modo) for prato in pratos_adicionais if prato.modo]
            reserva.modos_pratos_adicionais_passadas = modos_pratos_adicionais

        # Adicionar modos dos pratos adicionais ao contexto para reservas futuras
        for reserva in reservas_futuras:
            pratos_adicionais = reserva.pratos_adicionais_reserva.all()
            modos_pratos_adicionais = [(prato.food.name_food, prato.modo) for prato in pratos_adicionais if prato.modo]
            reserva.modos_pratos_adicionais_futuras = modos_pratos_adicionais
        
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
        email = request.POST.get('username_or_email')  # Agora capturamos o email
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me') == 'on'

        # Autenticar usuário com o email
        user = authenticate(request, username=email, password=password)  # Passamos o email como username

        if user is not None:
            # Login bem-sucedido
            login(request, user)
            if remember_me:
                # Defina um tempo de expiração mais longo para o login
                request.session.set_expiry(604800)  # 1 semana em segundos
            return redirect('index')  # Redireciona para a página de dashboard após o login
        else:
            # Login falhou
            return render(request, self.template_name, {'error_message': 'E-mail ou senha inválidos'})
    

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

        # Verifica se o e-mail já está cadastrado
        if User.objects.filter(email=email).exists():
            return render(request, self.template_name, {'error_message': 'Email já cadastrado. Por favor, escolha outro.'})

        # Cria um novo usuário com os detalhes fornecidos
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)

        # Redireciona para a página de login após o registro
        return redirect('login')


class redefinicao(TemplateView):
    template_name = "login/redefinicao.html"

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Verifica se o e-mail fornecido existe
        user = User.objects.filter(email=email).first()
        if not user:
            messages.error(request, 'E-mail não encontrado. Por favor, tente novamente.')
            return render(request, self.template_name)

        # Verifica se as senhas coincidem
        if new_password != confirm_password:
            messages.error(request, 'As senhas não coincidem. Por favor, tente novamente.')
            return render(request, self.template_name)

        # Define a nova senha para o usuário
        user.set_password(new_password)
        user.save()

        messages.success(request, 'Senha redefinida com sucesso.')
        return redirect('login')