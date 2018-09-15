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
        widgets = {
            'password': forms.PasswordInput(),
        }

class ProxyEdit(forms.ModelForm):
    def save(self, user, commit=True):
        proxy = super(ProxyEdit, self).save(commit=False)
        proxy.user=user
        if commit:
            proxy.save()
        return proxy
    class Meta:
        model = Proxy
        fields = ['name','url','username', 'password']

class MqttAdd(forms.ModelForm):
    class Meta:
        model = Mqtt
        fields = ['proxy','broker','QoS','topico']
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['broker'].queryset = Broker.objects.none()

class MqttEdit(forms.ModelForm):
    class Meta:
        model = Mqtt
        fields = ['broker','QoS','topico',]

class BrokerAdd(forms.ModelForm):
    class Meta:
        model = Broker
        fields = ['name','proxy','endereco', 'porta', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class BrokerEdit(forms.ModelForm):
    class Meta:
        model = Broker
        fields = ['name','proxy','endereco', 'porta', 'username', 'password']