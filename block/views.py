from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django_tables2 import RequestConfig
from django.views.generic import DeleteView

from block.forms import ProxyForm, BrokerForm, MqttAdd, MqttEdit, BrokerFormAdd
from block.models import Broker, Proxy,Mqtt
from block.tables import MqttTable
from block import task

@login_required
def tab_edit(request, proxy_id):
    template_name = 'block/forms/edit/tabEdit.html'
    proxy = get_object_or_404(Proxy, pk=proxy_id)
    context = {'proxy':proxy}
    return render(request, template_name, context)

@login_required
def add_proxy(request):
    template_name = 'block/forms/add/add_form.html'
    if request.method == 'POST':
        form = ProxyForm(request.POST)
        if form.is_valid():  # Vê se ta tudo okay
            proxy = form.save(commit=False)  # salva o usuário
            proxy.user = request.user
            proxy.save()
            task.conect_proxy.delay(proxy.pk)
            messages.success(
                request, 'Os dados do Proxy foram adicionados com sucesso'
            )
            return redirect('core:home')  # loga ele na sessão e retorna para a página definida no redirect login
    else:
        form = ProxyForm()
    context = {
        'form': form
    }
    return render(request, template_name, context)

@login_required
def add_mqtt(request):
    template_name = 'block/forms/add/mqtt_add.html'
    proxys = Proxy.objects.filter(user=request.user, status=1)
    if request.method == 'POST':
        form = MqttAdd(request.POST)
        if form.is_valid():  # Vê se ta tudo okay
            mqtt = form.save(commit=False)  # salva o usuário
            mqtts = Mqtt.objects.filter(broker=mqtt.broker, topico=mqtt.topico).exists()
            if mqtts == True:
                messages.error(
                    request, 'Já existe um Mqtt com este tópico para esse Proxy')
            else:
                messages.success(
                    request, 'Os dados do MQTT foram adicionados com sucesso'
                )
                mqtt.save()
                task.create_mqtt.delay(mqtt.pk)
                return redirect('core:home')  # loga ele na sessão e retorna para a página definida no redirect login
        else:
            form.fields['proxy'].queryset = proxys
    else:
        form = MqttAdd()
        form.fields['proxy'].queryset = proxys
        if proxys.exists():
            form.fields['broker'].queryset = Broker.objects.filter(proxy_id=proxys.first().pk)
    context = {
        'form': form
    }
    return render(request, template_name, context)

@login_required
def add_broker(request):
    template_name = 'block/forms/add/add_form.html'
    proxys = Proxy.objects.filter(user=request.user)
    if request.method == 'POST':
        form = BrokerFormAdd(request.POST)
        if form.is_valid():  # Vê se ta tudo okay
            broker = form.save()  # salva o usuário
            task.update_broker.delay(broker.pk)
            messages.success(
                request, 'Os dados do Broker foram adicionados com sucesso'
            )
            return redirect('core:home')  # loga ele na sessão e retorna para a página definida no redirect login
        else:
            form.fields['proxy'].queryset = proxys
    else:
        form = BrokerFormAdd()
        form.fields['proxy'].queryset = Proxy.objects.filter(user=request.user).all()
    context = {
        'form': form
    }
    return render(request, template_name, context)

@login_required
def edit_proxy(request, proxy_id):
    template_name = 'block/forms/edit/edit_form.html'
    context = {}
    proxy = get_object_or_404(Proxy, pk=proxy_id)
    if request.method == 'POST':
        form = ProxyForm(data=request.POST, instance=proxy)
        if form.is_valid():
            proxy = form.save(commit=False)
            proxy.user = request.user
            proxy.save()
            task.conect_proxy.delay(proxy.pk)
            messages.success(
                request, 'Os dados da sua conta foram alterados com sucesso'
            )
            return redirect('block:tab_edit', proxy.id)
    else:
        form = ProxyForm(instance=proxy)
        context['form'] = form
        context['proxy'] = proxy
        context['edit_proxy'] = "active"
    return render(request, template_name, context)

@login_required
def edit_broker(request, broker_id):
    template_name = 'block/forms/edit/edit_form.html'
    context = {}
    try:
        broker = Broker.objects.get(pk=broker_id)
    except:
        return render(request, 'block/404.html')
    if request.method == 'POST':
        form = BrokerForm(request.POST, instance=broker)
        if form.is_valid():
            broker = form.save()
            task.create_broker.delay(broker.pk)
            messages.success(
                request, 'Os dados da sua conta foram alterados com sucesso'
            )
            context = {'proxy': broker.proxy}
            return redirect('block:tab_edit', broker.proxy.id)
    else:
        form = BrokerForm(instance=broker)
        context['form'] = form
        context['broker'] = broker
    return render(request, template_name, context)


@login_required
def edit_mqtt(request, mqtt_id):
    template_name = 'block/forms/edit/mqtt_edit.html'
    context = {}
    mqttold = get_object_or_404(Mqtt, pk=mqtt_id)
    if request.method == 'POST':
        form = MqttEdit(request.POST)
        if form.is_valid():
            mqttnew = form.save(commit=False)
            mqtts = Mqtt.objects.filter(broker=mqttnew.broker, topico=mqttnew.topico).exists()
            if mqtts == True:
                messages.error(
                    request, 'Já existe um Mqtt com este tópico para esse Proxy')
                return redirect('block:tab_edit', mqttold.proxy.id)
            else:
                print(mqttold.topico)
                mqttnew.pk = mqttold.pk
                mqttnew.save()
                task.update_mqtt.delay(mqttnew.pk)
                messages.success(
                    request, 'Os dados do MQTT foram alterados com sucesso'
                )
                return redirect('block:tab_edit', mqttnew.proxy.id)
    else:
        form = MqttEdit(instance=mqttold)
        context['form'] = form
        context['proxy'] = mqttold.proxy
    return render(request, template_name, context)


def load_mqtt(request, broker_id):
    template_name = "block/mqtt_tab.html"
    mqtt = MqttTable(Mqtt.objects.filter(broker=broker_id).all())
    RequestConfig(request, paginate={'per_page': 5}).configure(mqtt)
    return render(request, template_name,{'mqtts':mqtt})


def load_broker(request):
    proxy_id = request.GET.get('proxy')
    brokers = Broker.objects.filter(proxy_id=proxy_id)
    return render(request, 'block/dropdown.html', {'dados': brokers})


@method_decorator(login_required, name='dispatch')
class ViewDeleteProxy(DeleteView):
    template_name = 'block/forms/delete/delete_form.html'
    model = Proxy
    # Notice get_success_url is defined here and not in the model, because the model will be deleted
    def get_success_url(self):
        messages.success(
            self.request, 'Deletado com sucesso!'
        )
        return reverse('core:home')


@method_decorator(login_required, name='dispatch')
class ViewDeleteBroker(DeleteView):
    template_name = 'block/forms/delete/delete_form.html'
    model = Broker
    def get_success_url(self):
        messages.success(
            self.request, 'Deletado com sucesso!'
        )
        return reverse('core:home')


@method_decorator(login_required, name='dispatch')
class ViewDeleteMqtt(DeleteView):
    template_name = 'block/forms/delete/delete_form.html'
    model = Mqtt
    def get_success_url(self):
        messages.success(
            self.request, 'Deletado com sucesso!'
        )
        return reverse('core:home')