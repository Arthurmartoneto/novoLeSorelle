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
    
    HORARIOS_CHOICES = [
        ('08:00', '08:00'),
        ('09:00', '09:00'),
        ('10:00', '10:00'),
        # Adicione mais horários conforme necessário
        ('20:00', '20:00'),
    ]

    # Defina o campo 'horario' usando as opções predefinidas
    horario = models.CharField(max_length=5, choices=HORARIOS_CHOICES)
    
    name_completo = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)  # Certifique-se de que o modelo Food esteja importado corretamente
    peso = models.CharField(max_length=10, null=True)
    date = models.DateField(null=True)
    hora = models.CharField(choices=HORARIOS_CHOICES, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.food.name_food} - {self.date} {self.hora}"
