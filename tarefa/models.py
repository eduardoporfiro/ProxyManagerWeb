from django.db import models
from block.models import Mqtt, Proxy
from core.models import AbstractDispositivo, AbstractDado, Task

class Dispositivo(AbstractDispositivo):
    mqtt = models.OneToOneField(Mqtt, on_delete=models.CASCADE)
    proxy = models.ForeignKey(Proxy, on_delete=models.CASCADE, blank=True)
    def __str__(self):
        return self.nome


class Dado (AbstractDado):
     sensor = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)

class Job(models.Model):
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    workspace = models.TextField()
    last_update = models.DateTimeField(auto_now=True)
    firs_task = models.ForeignKey(Task, on_delete=models.CASCADE)