from django_tables2 import RequestConfig
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

from block.models import Mqtt, Proxy

from .tables import DispositivoTable
from .models import Dispositivo
from .forms import DispositivoForm, DispositivoAddForm

@login_required
def load_dispositivo(request, proxy_id):
    template_name = "tarefa/dispositivo_tab.html"
    dispositivo = DispositivoTable(Dispositivo.objects.filter(proxy=proxy_id).all())
    RequestConfig(request).configure(dispositivo)
    return render(request, template_name, {'dispositivos': dispositivo})

@login_required
def add_dispositivo(request, mqtt_id):
    template_name = 'tarefa/form_dispos.html'
    if request.method == 'POST':
        form = DispositivoForm(request.POST)
        if form.is_valid():  # Vê se ta tudo okay
            dispositivo = form.save(commit=False)  # salva o usuário
            dispositivo.proxy= dispositivo.mqtt.broker.proxy
            dispositivo.save()
            messages.success(
                request, 'Os dados do Proxy foram adicionados com sucesso'
            )
            return redirect('core:home')  # loga ele na sessão e retorna para a página definida no redirect login
    else:
        try:
            dispo = Dispositivo.objects.get(mqtt=mqtt_id)
        except Dispositivo.DoesNotExist:
            dispo = Dispositivo(mqtt=Mqtt.objects.get(pk=mqtt_id))
            form = DispositivoForm(instance=dispo)
            context = {
                'form': form,
                'existe': 'N'
            }
            return render(request, template_name, context)
        form = DispositivoForm(instance=dispo)
        context = {
            'form': form,
            'existe': 'S'
        }
    return render(request, template_name, context)

@login_required
def add_dispositivo(request):
    template_name = 'tarefa/add_dispositivo.html'
    proxys = Proxy.objects.filter(user=request.user)
    if request.method == 'POST':
        form = DispositivoAddForm(request.POST)
        if form.is_valid():  # Vê se ta tudo okay
            dispositivo = form.save(commit=False)  # salva o usuário
            dispositivo.proxy= dispositivo.mqtt.broker.proxy
            dispositivo.save()
            messages.success(
                request, 'Os dados do Proxy foram adicionados com sucesso'
            )
            return redirect('core:home')  # loga ele na sessão e retorna para a página definida no redirect login
    else:
        form = DispositivoAddForm()
        form.fields['proxy'].queryset = proxys
        form.fields['mqtt'].queryset = Mqtt.objects.filter(proxy_id=proxys.first().pk)
        context = {
            'form': form,
            'existe': 'N'
        }
        return render(request, template_name, context)

@login_required
def edit_dispositivo(request, dispo_id):
    template_name = 'tarefa/form_dispos.html'
    proxys = Proxy.objects.filter(user=request.user)
    form = DispositivoForm(request.POST)
    if form.is_valid():  # Vê se ta tudo okay
        dispositivo = form.save(commit=False)  # salva o usuário
        dispositivo.proxy = dispositivo.mqtt.broker.proxy
        dispositivo.save()
        messages.success(
            request, 'Os dados do Proxy foram adicionados com sucesso'
        )
        return redirect('core:home')  # loga ele na sessão e retorna para a página definida no redirect logi
    else:
        dispo = get_object_or_404(Dispositivo, pk=dispo_id)
        form = DispositivoForm(instance=dispo)
        form.fields['proxy'].queryset = proxys
        form.fields['mqtt'].queryset = Mqtt.objects.filter(proxy_id=proxys.first().pk)
        context = {
            'form': form,
            'existe': 'S'
        }
    return render(request, template_name, context)

@login_required
def load_mqtt(request):
    proxy_id = request.GET.get('proxy')
    mqtts = Mqtt.objects.filter(proxy_id=proxy_id)
    return render(request, 'tarefa/dropdown_dispo.html', {'mqtts': mqtts})

def index(request):
    template = loader.get_template('tarefa/index.html')
    context = {

    }
    return HttpResponse(template.render(context, request))