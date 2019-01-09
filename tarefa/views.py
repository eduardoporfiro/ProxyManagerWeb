from django_tables2 import RequestConfig
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.generic import DeleteView
from django.views.decorators.csrf import csrf_exempt
import datetime

from block.models import Mqtt, Proxy

from .tables import DispositivoTable, DadoTable
from .models import Dispositivo, Job, Dado
from .forms import DispositivoForm, DispositivoAddForm
import tarefa.task as celery
import json

from .utils import tarefas
from.resources import DadoResource


@login_required
def load_dispositivo(request, proxy_id):
    template_name = "tarefa/dispositivo_tab.html"
    dispositivo = DispositivoTable(Dispositivo.objects.filter(proxy=proxy_id).all())
    RequestConfig(request, paginate={'per_page': 5}).configure(dispositivo)
    return render(request, template_name, {'dispositivos': dispositivo})


@login_required
def load_dado_graph(request, dispo_id):
    template_name = "tarefa/dado_tab.html"
    dispo = Dispositivo.objects.filter(pk=dispo_id).get()
    dado = Dado.objects.filter(sensor=dispo_id).all()
    if dispo.is_int:
        valor = [int(obj.valor_int) for obj in dado]
    else:
        valor =[obj.valor_char for obj in dado]
    id = [obj.id for obj in dado]
    dados = {'dado': valor, 'id': id}
    return HttpResponse(json.dumps(dados))


@login_required
def load_dado(request, dispo_id):
    template_name = "tarefa/dado_tab.html"
    dispo = Dispositivo.objects.filter(pk=dispo_id).get()
    dado = DadoTable(Dado.objects.filter(sensor=dispo_id).all())
    RequestConfig(request, paginate={'per_page': 10}).configure(dado)
    return render(request, template_name, {'dado': dado, 'dispo': dispo})


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
        if proxys.exists():
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
    mqtts = Mqtt.objects.filter(proxy_id=proxy_id, dispositivo__isnull=True)
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
    if request.method == 'POST':
        dispositivo = get_object_or_404(Dispositivo, pk=dispo_id)
        try:
            job = dispositivo.job
            celery.delete_task.delay(job.firs_task.proxy_alt_id, dispositivo.proxy.pk)
            job.firs_task.delete()
            celery.delete_job.delay(job.proxy_alt_id, dispositivo.proxy.url, dispositivo.proxy.token)
            job.delete()
        except:
            pass
        job = Job(dispositivo=dispositivo)
        tarefa = request.POST['code']
        work = request.POST['work']
        tasks = tarefas(tarefa, dispositivo.proxy.pk)
        job.workspace=work
        job.proxy = dispositivo.proxy
        try:
            job.firs_task = tasks[0]
        except IndexError:
            pass
        if job.pk is None:
            job.save()
            celery.create_job.delay(job.pk)
        else:
            job.save()
            celery.edit_job.delay(job.pk)
    return HttpResponse(request, 'OKAY')


def get_xml(request, pk):
    dispo = Dispositivo.objects.get(pk=pk)
    try:
        job = dispo.job
    except:
        job = Job()
    return HttpResponse(job.workspace, content_type = 'text')


@login_required
def export_dado_excel(request, id_sensor):
    dado_resource = DadoResource()
    queryset = Dado.objects.filter(sensor=id_sensor)
    dataset = dado_resource.export(queryset)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="dados_{}.xls"'.format(datetime.datetime.now().strftime('%H:%M:%S_%d_%m_%Y'))
    return response
