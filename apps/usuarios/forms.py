from django import forms

from .models import PerfilUsuario


class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['rol', 'telefono']
        widgets = {
            'rol': forms.Select(attrs={'class': 'block w-full rounded-md border-gray-300 shadow-sm text-sm'}),
            'telefono': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm text-sm',
                'placeholder': '10 dígitos',
            }),
        }
        labels = {
            'rol': 'Rol en el sistema',
            'telefono': 'Teléfono de contacto',
        }
