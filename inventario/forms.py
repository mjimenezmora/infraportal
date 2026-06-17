from django import forms
from .models import *

class ServidorVirtualForm(forms.ModelForm):
    class Meta:
        model = ServidorVirtual
        fields = "__all__"

        widgets = {
            # Ajustado a minúscula para coincidir con tu modelo
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            # Agregamos clases de Bootstrap a los demás para que no se vean planos
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'ip_int': forms.TextInput(attrs={'class': 'form-control'}),
            'ip_ext': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ServidorFisicoForm(forms.ModelForm):
    class Meta:
        model = ServidorFisico
        fields = "__all__"

        widgets = {
            # Ajustado a minúscula para coincidir con tu modelo
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            # Agregamos clases de Bootstrap a los demás para que no se vean planos
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'ip_int': forms.TextInput(attrs={'class': 'form-control'}),
            #'ip_ext': forms.TextInput(attrs={'class': 'form-control'}),
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

# Formulario de Sistema Operativo

class SistemaOperativoForm(forms.ModelForm):
    class Meta:
        model = SistemaOperativo
        fields = '__all__'
        widgets = {
            'nombre' : forms.TextInput(attrs={'class': 'form-control'}),
            #'version' : forms.TextInput(attrs={'class' : 'form-control'}),
        }

class CredencialForm(forms.ModelForm):
    # MODIFICADO: Cambiado a ModelMultipleChoiceField para permitir seleccionar varias
    credencial_existente = forms.ModelMultipleChoiceField(
        queryset=CredencialServidor.objects.all(),
        required=False,
        label="Seleccionar credencial(es) existente(s)",
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input',
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control caja-descripcion-reducida', # <-- Aquí enganchamos tu CSS personalizado
                'rows': 2,
                'placeholder': 'Ej: Acceso exclusivo para el Administrador de la BD'
            }),
            #'size': '6', # Define cuántas filas se ven de un vistazo
            #'style': 'height: 160px;' # Altura cómoda para clics múltiples
        }),
        help_text="Mantén presionado Ctrl (en Windows) o Cmd (en Mac) para seleccionar más de una."
    )

    class Meta:
        model = CredencialServidor
        fields = ['tipo_acceso', 'usuario', 'password', 'puerto', 'descripcion']
        widgets = {
            'password': forms.PasswordInput(render_value=True, attrs={'class': 'form-control'}),
            'tipo_acceso': forms.Select(attrs={'class': 'form-select'}),
            'usuario': forms.TextInput(attrs={'class': 'form-control'}),
            'puerto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 22'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_acceso'].required = False
        self.fields['usuario'].required = False
        self.fields['password'].required = False