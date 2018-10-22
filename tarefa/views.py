from django_tables2 import RequestConfig
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.template import loader
from django.views.generic import DeleteView
from django.views.decorators.csrf import csrf_exempt

from block.models import Mqtt, Proxy

from .tables import DispositivoTable
from .models import Dispositivo, Job
from .forms import DispositivoForm, DispositivoAddForm
import tarefa.task as celery

from .utils import tarefas


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
            celery.create_dispo.delay(dispositivo.pk)
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
    proxys = Proxy.objects.filter(user=request.user, status=1)
    if request.method == 'POST':
        form = DispositivoAddForm(request.POST)
        if form.is_valid():  # Vê se ta tudo okay
            dispositivo = form.save(commit=False)  # salva o usuário
            dispositivo.proxy= dispositivo.mqtt.broker.proxy
            dispositivo.save()
            celery.create_dispo.delay(dispositivo.pk)
            messages.success(
                request, 'Os dados do Proxy foram adicionados com sucesso'
            )
            return redirect('core:home')  # loga ele na sessão e retorna para a página definida no redirect login
        return render(request, template_name, {'form': form})
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
    if request.method == 'POST':
        form = DispositivoForm(request.POST)
        if form.is_valid():  # Vê se ta tudo okay
            dispositivo = form.save(commit=False)  # salva o usuário
            dispo = Dispositivo.objects.filter(mqtt=dispositivo.mqtt)
            dispo = dispositivo
            dispositivo.proxy = dispositivo.mqtt.broker.proxy
            dispositivo.save()
            celery.edit_dispo.delay(dispositivo.pk)
            messages.success(
                request, 'Os dados do Proxy foram alterados com sucesso'
            )
            return redirect('core:home')  # loga ele na sessão e retorna para a página definida no redirect logi
        return render(request, template_name, {'form': form})
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


def index(request, pk):
    dispositivo = get_object_or_404(Dispositivo, pk=pk)
    atuadores = Dispositivo.objects.filter(proxy=dispositivo.proxy, tipo=0)
    sensores = Dispositivo.objects.filter(proxy=dispositivo.proxy, tipo=1)
    template = loader.get_template('tarefa/index.html')
    context = {
        'dispositivo': dispositivo,
        'atuadores': atuadores,
        'sensores': sensores,
    }
    return HttpResponse(template.render(context, request))


@csrf_exempt
@login_required
def post_task(request, dispo_id):
    if request.method=='POST':
        dispositivo = get_object_or_404(Dispositivo, pk=dispo_id)
        try:
            job = dispositivo.job
            celery.delete_task(job.firs_task.proxy_alt_id, dispositivo.proxy.pk)
            job.firs_task.delete()
        except:
            job = Job(dispositivo=dispositivo)
        tarefa = request.POST['code']
        work = request.POST['work']
        tasks = tarefas(tarefa, dispositivo.proxy.pk)
        job.workspace=work
        job.firs_task = tasks[0]
        job.save()
        celery.create_job.delay(job.pk)
    return HttpResponse(request, 'OKAY')


def get_xml(request, pk):
    dispo = Dispositivo.objects.get(pk=pk)
    try:
        job = dispo.job
    except:
        job = Job()
    return HttpResponse(job.workspace, content_type = 'text')

