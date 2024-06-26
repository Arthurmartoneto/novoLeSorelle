from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_init

def set_email_unique(instance, **kwargs):
    instance._meta.get_field('email')._unique = True

post_init.connect(set_email_unique, sender=User)

class Food(models.Model):
    STATUS_CHOICES = (
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
    )
    
    name_food = models.CharField(max_length=100)
    img = models.ImageField(upload_to='foods/')  # Você precisará do pacote Pillow instalado para usar ImageField
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativo')

    def __str__(self):
        return self.name_food


class Reserva(models.Model):
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('em_preparo', 'Em Preparo'),
        ('pronto', 'Pronto'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    )
    
    MODO_CHOICES = (
        ('fresco', 'Fresco'),
        ('congelado', 'Congelado'),
        ('Aquecido', 'Aquecido'),
    )
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='reservas_principal')
    peso = models.CharField(max_length=10, null=True)
    modo = models.CharField(max_length=10, choices=MODO_CHOICES, null=True)
    date = models.DateField(null=True)
    hora = models.CharField(null=True, max_length=10)    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    
    def __str__(self):
        return f"{self.usuario.username} - {self.food.name_food} - {self.date} {self.hora}"

    def get_email(self):
        return self.usuario.email
    
class PratoAdicional(models.Model):
    MODO_CHOICES = (
        ('fresco', 'Fresco'),
        ('congelado', 'Congelado'),
        ('aquecido', 'Aquecido'),
    )
    
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='pratos_adicionais_reserva')
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='pratos_adicionais_food')
    peso = models.CharField(max_length=10, null=True)
    modo = models.CharField(max_length=10, choices=MODO_CHOICES, null=True)

    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Adicionando campo valor


class Notification(models.Model):
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.subject   
    
    
class Blog(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.URLField(max_length=200)
    img = models.ImageField(upload_to='blog/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description[:50]  # Retorna os primeiros 50 caracteres da descrição como representação do objeto
