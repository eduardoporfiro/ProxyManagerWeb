from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import  CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from block.forms import ProxyAdd, ProxyEdit, BrokerAdd, BrokerEdit, MqttAdd, MqttEdit
from block.models import Dado, Broker, Proxy,Mqtt

def index(request):
    testes = Dado.objects.filter(user=request.User).all()
    template = loader.get_template('block/index.html')
    context = {
        'testes': testes,
    }
    return HttpResponse(template.render(context, request))


@login_required
def add_proxy(request):
    template_name = 'block/add_form.html'
    if request.method == 'POST':
        form = ProxyAdd(request.POST)
        if form.is_valid():  # Vê se ta tudo okay
            proxy = form.save(request.user)  # salva o usuário
            return redirect('core:home')  # loga ele na sessão e retorna para a página definida no redirect login
    else:
        form = ProxyAdd()
    context = {
        'form': form
    }
    return render(request, template_name, context)

@login_required
def edit_proxy(request):
    template_name = 'block/edit_form.html'
    context = {}
    if request.method == 'POST':
        form = ProxyEdit(request.POST)
        if form.is_valid():

            form.save()
            messages.success(
                request, 'Os dados da sua conta foram alterados com sucesso'
            )
            return redirect('accounts:dashboard')
    else:
        form = ProxyEdit(instance=request.user)
    context['form'] = form
    return render(request, template_name, context)


@login_required
def edit_broker(request):
    template_name = 'block/edit_form.html'
    context = {}
    if request.method == 'POST':
        form = BrokerEdit(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Os dados da sua conta foram alterados com sucesso'
            )
            return redirect('accounts:dashboard')
    else:
        form = BrokerAdd()
        form.fields['proxy'].queryset = Proxy.objects.filter(user=request.user)
    context['form'] = form
    return render(request, template_name, context)

@login_required
def add_broker(request):
    template_name = 'block/add_form.html'
    if request.method == 'POST':
        form = BrokerAdd(request.POST)
        if form.is_valid():  # Vê se ta tudo okay
            broker = form.save()  # salva o usuário
            return redirect('core:home')  # loga ele na sessão e retorna para a página definida no redirect login
    else:
        form = BrokerAdd()
        form.fields['proxy'].queryset = Proxy.objects.filter(user=request.user)
    context = {
        'form': form
    }
    return render(request, template_name, context)



@login_required
def edit_mqtt(request):
    template_name = 'block/edit_form.html'
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
    return render(request, template_name, context)


class MqttCreateView(LoginRequiredMixin, CreateView):
    model = Mqtt
    form_class = MqttAdd
    template_name = 'block/mqtt_add.html'
    success_url = reverse_lazy('core:home')

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        form.fields['proxy'].queryset = Proxy.objects.filter(user=request.user)
        return render(request, self.template_name, {'form': form})


def load_broker(request):
    proxy_id = request.GET.get('proxy')
    brokers = Broker.objects.filter(proxy_id=proxy_id)
    return render(request, 'block/dropdown_mqtt.html', {'brokers': brokers})