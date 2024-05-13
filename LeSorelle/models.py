from django.db import models
from django.contrib.auth.models import User


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
    )
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)  # Certifique-se de que o modelo Food esteja importado corretamente
    peso = models.CharField(max_length=10, null=True)
    date = models.DateField(null=True, max_length=10)
    hora = models.CharField(null=True, max_length=10)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    def __str__(self):
        return f"{self.user.username} - {self.food.name_food} - {self.date} {self.hora}"

    def get_email(self):
        return self.usuario.email