from django import forms
from block.models import Mqtt, Proxy,Broker

class ProxyForm(forms.ModelForm):
    class Meta:
        model = Proxy
        fields = ['name','url','username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

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
        fields = ['proxy', 'broker', 'QoS', 'topico']

class BrokerForm(forms.ModelForm):
    class Meta:
        model = Broker
        fields = ['name','endereco', 'porta', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
