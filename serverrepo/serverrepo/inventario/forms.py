from django import forms
from .models import *

class ServidorVirtualForm(forms.ModelForm):

    class Meta:
        model = ServidorVirtual
        fields = "__all__"

        widgets = {
            'Descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }

class PasswordGen(forms.Form):  # <--- Cambia ModelForm por Form
    numero = forms.IntegerField(
        label="Número de contraseñas",
        min_value=1,
        max_value=50,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    longitud = forms.IntegerField(
        label="Longitud",
        min_value=8,
        max_value=32,
        initial=16,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    caracter = forms.CharField(
        label="Caracteres a omitir",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: @#$'})
    )