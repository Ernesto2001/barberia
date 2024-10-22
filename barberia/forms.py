from django import forms
from tasks.models import TipoServicio

class TipoServicioForm(forms.ModelForm):
    class Meta:
        model = TipoServicio
        fields = ['nombre']
