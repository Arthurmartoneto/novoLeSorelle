from django.db import models
from django.contrib.auth.models import User


class Food(models.Model):
    PESO_CHOICES = (
        ('400g', '400g'),
        ('500g', '500g'),
        ('1KG', '1KG'),
    )
    
    name_food = models.CharField(max_length=100)
    img = models.ImageField(upload_to='foods/')  # Você precisará do pacote Pillow instalado para usar ImageField
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    peso = models.CharField(max_length=4, choices=PESO_CHOICES)

    def __str__(self):
        return self.name_food


class Reserva(models.Model):
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)  # Certifique-se de que o modelo Food esteja importado corretamente
    peso = models.CharField(max_length=10, null=True)
    date = models.DateField(null=True, max_length=10)
    hora = models.CharField(null=True, max_length=10)

    def __str__(self):
        return f"{self.user.username} - {self.food.name_food} - {self.date} {self.hora}"
