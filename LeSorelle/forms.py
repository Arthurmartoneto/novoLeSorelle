from django import forms
from .models import Reserva, Food, Blog

class ReservaForm(forms.ModelForm):
    PESO_CHOICES = [
        ('', 'Peso'),
        ('400g', '400g'),
        ('500g', '500g'),
        ('1000g', '1000g'),
    ]
    
    HORARIOS_CHOICES = [
        ('', 'Horario de Retirada'),
        ('09:00', '09:00'),
        ('10:00', '10:00'),
        ('11:00', '11:00'),
        ('12:00', '12:00'),
        ('13:00', '13:00'),
        ('14:00', '14:00'),
        ('15:00', '15:00'),
        ('16:00', '16:00'),
        ('17:00', '17:00'),
        ('18:00', '18:00'),
        ('19:00', '19:00'),
    ]
    
    peso = forms.ChoiceField(choices=PESO_CHOICES, widget=forms.Select(attrs={'class': 'selectpicker form-control'}))
    hora = forms.ChoiceField(choices=HORARIOS_CHOICES, widget=forms.Select(attrs={'class': 'selectpicker form-control'}))
   
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = Reserva
        fields = ['telefone', 'food', 'peso', 'date', 'hora', 'modo']
        widgets = {
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'id': 'telefone'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'food': forms.Select(attrs={'class': 'selectpicker form-control'}),
            'modo': forms.Select(attrs={'class': 'selectpicker form-control'}),
        }



class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name_food', 'descricao', 'valor', 'img']
        widgets = {
            'name_food': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
            'img': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        
        
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['link', 'description', 'img']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'link': forms.URLInput(attrs={'class': 'form-control'}),
            'img': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }