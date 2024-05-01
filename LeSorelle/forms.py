from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    PESO_CHOICES = [
        ('400g', '400g'),
        ('500g', '500g'),
        ('1KG', '1KG'),
    ]

    peso = forms.ChoiceField(choices=PESO_CHOICES, widget=forms.Select(attrs={'class': 'selectpicker form-control'}))
    hora = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'class': 'form-control', 'placeholder': 'Horário'}))
    

    class Meta:
        model = Reserva
        fields = ['name_completo', 'email', 'telefone', 'food', 'peso', 'date', 'hora']
        widgets = {
            'name_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'id': 'telefone'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'food': forms.Select(attrs={'class': 'selectpicker form-control'}),
        }
