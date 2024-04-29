from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['name_completo', 'email', 'telefone', 'food', 'peso', 'date', 'hora']