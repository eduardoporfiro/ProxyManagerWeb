from django.db import models
from block.models import Mqtt, Proxy
from core.models import AbstractDispositivo, AbstractDado

class Dispositivo(AbstractDispositivo):
    mqtt = models.OneToOneField(Mqtt, on_delete=models.CASCADE)
    proxy = models.ForeignKey(Proxy, on_delete=models.CASCADE, blank=True)
    def __str__(self):
        return self.nome


class Dado (AbstractDado):
     sensor = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)

