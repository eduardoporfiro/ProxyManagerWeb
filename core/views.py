from django.shortcuts import render
from tarefa.models import Dado, Dispositivo, Proxy, Mqtt
from tarefa.tables import DadoTable


def home(request):
    dispo = Dispositivo.objects.all()
    proxys = Proxy.objects.filter(user=request.user).all()
    mqtts = Mqtt.objects.all()
    context = {
        'dispos': dispo,
        'proxys': proxys,
        'mqtts': mqtts,
    }
    return render(request, 'core/home.html', context=context)
