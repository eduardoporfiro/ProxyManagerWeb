from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import  CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from block.forms import ProxyForm, BrokerForm, MqttAdd, MqttEdit
from block.models import Dado, Broker, Proxy,Mqtt
from accounts.models import User


def index(request):
    testes = Dado.objects.filter(user=request.User).all()
    template = loader.get_template('block/index.html')
    context = {
        'testes': testes,
    }
    return HttpResponse(template.render(context, request))

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
    proxys = Proxy.objects.filter(user=request.user)
    if request.method == 'POST':
        form = MqttAdd(request.POST)
        if form.is_valid():  # Vê se ta tudo okay
            mqtt = form.save()  # salva o usuário
            messages.success(
                request, 'Os dados do MQTT foram adicionados com sucesso'
            )
            return redirect('core:home')  # loga ele na sessão e retorna para a página definida no redirect login
        else:
            form.fields['proxy'].queryset = proxys
    else:
        form = MqttAdd()
        form.fields['proxy'].queryset = proxys
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
        form = BrokerForm(request.POST)
        if form.is_valid():  # Vê se ta tudo okay
            broker = form.save()  # salva o usuário
            messages.success(
                request, 'Os dados do Broker foram adicionados com sucesso'
            )
            return redirect('core:home')  # loga ele na sessão e retorna para a página definida no redirect login
        else:
            form.fields['proxy'].queryset = proxys
    else:
        form = BrokerForm()
        form.fields['proxy'].queryset = proxys
    context = {
        'form': form
    }
    return render(request, template_name, context)

@login_required
def edit_proxy(request, proxy_id):
    template_name = 'block/forms/edit/edit_form.html'
    context = {}
    proxy = Proxy.objects.get(pk=proxy_id)
    if request.method == 'POST':
        proxy = get_object_or_404(Proxy, pk=proxy_id)
        form = ProxyForm(data=request.POST, instance=proxy)
        if form.is_valid():
            proxy = form.save(commit=False)
            proxy.user = request.user
            proxy.save()
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
    broker = Broker.objects.get(pk=broker_id)
    if request.method == 'POST':
        form = BrokerForm(request.POST, instance=broker)
        if form.is_valid():
            broker = form.save()
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
    template_name = 'block/forms/edit/edit_form.html'
    context = {}
    if request.method == 'POST':
        form = MqttEdit(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Os dados da sua conta foram alterados com sucesso'
            )
            return redirect('accounts:dashboard')
    else:
        form = MqttEdit()
        #form.fields['broker'] = Broker.objects.filter
    context['form'] = form
    context['edit_mqtt'] = "active"
    return render(request, template_name, context)


def load_broker(request):
    proxy_id = request.GET.get('proxy')
    brokers = Broker.objects.filter(proxy_id=proxy_id)
    return render(request, 'block/dropdown_mqtt.html', {'brokers': brokers})