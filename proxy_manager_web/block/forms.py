from django import forms
from block.models import Mqtt, Proxy,Broker

class ProxyAdd(forms.ModelForm):
    def save(self, user, commit=True):
        proxy = super(ProxyAdd, self).save(commit=False)
        proxy.user=user
        if commit:
            proxy.save()
        return proxy
    class Meta:
        model = Proxy
        fields = ['name','url','username', 'password']

class ProxyEdit(forms.ModelForm):
    class Meta:
        model = Proxy
        fields = ['name','url','username', 'password']

class MqttAdd(forms.ModelForm):
    class Meta:
        model = Mqtt
        fields = ['broker','QoS','topico',]

class MqttEdit(forms.ModelForm):
    class Meta:
        model = Mqtt
        fields = ['broker','QoS','topico',]

class BrokerAdd(forms.ModelForm):
    class Meta:
        model = Broker
        fields = ['name','proxy','endereco', 'porta', 'username', 'password']

class BrokerEdit(forms.ModelForm):
    class Meta:
        model = Broker
        fields = ['name','proxy','endereco', 'porta', 'username', 'password']