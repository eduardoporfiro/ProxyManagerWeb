from django.db import models
from block.models import Mqtt, Proxy

class Dispositivo(models.Model):
    TIPO = (
        (0, 'Atuador'),
        (1, 'Sensor'),
    )
    nome = models.CharField(max_length=200)
    mqtt = models.OneToOneField(Mqtt, on_delete=models.CASCADE)
    proxy = models.ForeignKey(Proxy, on_delete=models.CASCADE, blank=True)
    tipo = models.IntegerField(choices=TIPO, default=0)

class Dado (models.Model):
     sensor = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
     valor_char = models.CharField(max_length=500, blank=True)
     valor_int = models.IntegerField(blank=True)
