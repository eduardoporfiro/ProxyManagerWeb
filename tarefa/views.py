from django_tables2 import RequestConfig
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.template import loader
from django.views.generic import DeleteView

from block.models import Mqtt, Proxy, Broker

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
def add_dispositivos(request, mqtt_id):
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
            form.fields['mqtt'].queryset = Mqtt.objects.filter(pk=mqtt_id).all()
            context = {
                'form': form,
                'existe': 'N'
            }
            return render(request, template_name, context)
        form = DispositivoForm(instance=dispo)
        form.fields['mqtt'].queryset = Mqtt.objects.filter(pk=mqtt_id).all()
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
        form.fields['mqtt'].queryset = Mqtt.objects.filter(proxy_id=proxys.first().pk)
        context = {
            'form': form,
            'existe': 'S'
        }
    return render(request, template_name, context)

@method_decorator(login_required, name='dispatch')
class ViewDeleteDispo(DeleteView):
    template_name = 'block/forms/delete/delete_form.html'
    model = Dispositivo
    # Notice get_success_url is defined here and not in the model, because the model will be deleted
    def get_success_url(self):
        messages.success(
            self.request, 'Deletado com sucesso!'
        )
        return reverse('core:home')

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