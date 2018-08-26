from django import forms
from block.models import Mqtt, Proxy

class ProxyAdd(forms.ModelForm):
    class Meta:
        model = Proxy
        fields = ['name','url','user', 'password']

class ProxyEdit(forms.ModelForm):
    class Meta:
        model = Proxy
        fields = ['name','url','user', 'password']