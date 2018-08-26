from core.models import *
from django.conf import settings
from django.db import models

class Proxy(models.Model):
    name = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=150, blank=False)
    user = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class Broker(AbstractBroker):
    name = models.CharField(max_length=100, blank=True)
    proxy = models.ForeignKey(Proxy, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Mqtt(AbstractMqtt):
    broker = models.ForeignKey(Broker, on_delete=True, related_name='mqtt')
    def __str__(self):
        return self.topico

class Dado(AbstractDado):
    mqtt = models.ForeignKey(Mqtt, on_delete=models.CASCADE, editable=False, related_name='dado')

class Relation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
        related_name='relation', on_delete=models.CASCADE
    )
    proxy = models.ForeignKey(
        Proxy, verbose_name='Proxy', related_name='enrollments',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        unique_together = (('user', 'proxy'),)
