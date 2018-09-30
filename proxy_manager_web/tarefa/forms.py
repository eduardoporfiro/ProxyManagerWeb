from django import forms
from tarefa.models import Dispositivo

class DispositivoForm(forms.ModelForm):
    class Meta:
        model = Dispositivo
        fields = ['nome','mqtt','tipo']

class DispositivoAddForm(forms.ModelForm):
    class Meta:
        model = Dispositivo
        fields = ['nome','proxy','mqtt','tipo']