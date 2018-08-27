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
        fields = ['proxy','broker','QoS','topico',]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['broker'].queryset = Broker.objects.none()

        if 'broker' in self.data:
            try:
                proxy_id = int(self.data.get('proxy'))
                self.fields['broker'].queryset = Broker.objects.filter(proxy_id=proxy_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['broker'].queryset = self.instance.proxy.broker.order_by('name')

class MqttEdit(forms.ModelForm):
    class Meta:
        model = Mqtt
        fields = ['proxy','broker','QoS','topico',]

class BrokerAdd(forms.ModelForm):
    class Meta:
        model = Broker
        fields = ['name','proxy','endereco', 'porta', 'username', 'password']

class BrokerEdit(forms.ModelForm):
    class Meta:
        model = Broker
        fields = ['name','proxy','endereco', 'porta', 'username', 'password']