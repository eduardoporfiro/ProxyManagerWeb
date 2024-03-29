from django.db import models
from block.models import Mqtt, Proxy
from core.models import AbstractDispositivo, AbstractDado


class Dispositivo(AbstractDispositivo):
    mqtt = models.OneToOneField(Mqtt, on_delete=models.CASCADE)
    proxy = models.ForeignKey(Proxy, on_delete=models.CASCADE, blank=True, related_name='dispositivo')

    def __str__(self):
        return self.nome


class Dado (AbstractDado):
     sensor = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)


class Settings(models.Model):
    Tipos = [
        (0, 'save_database'),
        (1, 'dado_sensor_numero'),
        (2, 'dado_sensor_string'),
        (3, 'dados_sensor_media'),
        (4, 'dado_sensor_min'),
        (5, 'dado_sensor_max'),
        (6, 'if_sensor_string'),
        (7, 'if_sensor_numero'),
        (8, 'if_sensor_boolean'),
        (9, 'if_sensor_dadosensor'),
        (10, 'atuador_troca_estado'),
        (11, 'atuador_boolean'),
        (12, 'if_else_sensor_string'),
        (13, 'if_else_sensor_boolena'),
        (14, 'if_else_sensor_dadosensor'),
        (15, 'if_else_sensor_number')
    ]
    task_tipo = models.IntegerField(choices=Tipos)
    url_create = models.CharField(max_length=200,  default='')
    url_update = models.CharField(max_length=200)

    def __str__(self):
        return self.url_create+'  '+self.url_update+'  '+str(self.task_tipo)


class Task(models.Model):
    tipo = models.ForeignKey(Settings, on_delete=models.CASCADE)
    comando = models.CharField(max_length=200)
    task_anterior = models.ForeignKey('self', on_delete=models.CASCADE,
                                      related_name='anterior', null=True, blank=True)
    task_sucessor = models.ForeignKey('self', on_delete=models.CASCADE,
                                      related_name='sucessor', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    proxy_alt_id = models.IntegerField(null=True)
    proxy = models.ForeignKey(Proxy, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.comando


class If_sensor_string(Task):
    Condicao = [
        (0, '='),
        (1, '!=')
    ]
    condicao = models.IntegerField(choices=Condicao)
    valor = models.CharField(max_length=200, null=True)


class If_sensor_numero(Task):
    Condicao = [
        (0, '='),
        (1, '!='),
        (2, '>'),
        (3, '>='),
        (4, '<'),
        (5, '<=')
    ]
    condicao = models.IntegerField(choices=Condicao)
    valor = models.IntegerField(null=True)


class If_sensor_boolean(Task):
    Condicao = [
        (0, '='),
        (1, '!=')
    ]
    condicao = models.IntegerField(choices=Condicao)
    valor = models.NullBooleanField()


class If_sensor_dadosensor(Task):
    Condicao = [
        (0, '='),
        (1, '!='),
        (2, '>'),
        (3, '>='),
        (4, '<'),
        (5, '<=')
    ]
    condicao = models.IntegerField(choices=Condicao)
    valor = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='If_sensor_dadosensor', null=True)


class Job(models.Model):
    dispositivo = models.OneToOneField(Dispositivo, on_delete=models.CASCADE, related_name='job')
    workspace = models.TextField()
    last_update = models.DateTimeField(auto_now=True)
    firs_task = models.ForeignKey(Task, on_delete=models.CASCADE)
    proxy_alt_id = models.IntegerField(null=True)
    proxy = models.ForeignKey(Proxy, on_delete=models.CASCADE, null=True)

    def delete(self, using=None, keep_parents=False):
        self.firs_task.delete()
        super(Job, self).delete()

    def __str__(self):
        return 'Job: '+self.dispositivo.nome


class Atuador_troca_estado(Task):
    estado_anterior = models.BooleanField(default=True, null=True)
    estado_atual = models.BooleanField(default=False, null=True)
    atuador = models.ForeignKey(Dispositivo, on_delete=models.CASCADE,  null=True)
    
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.estado_anterior is None:
            self.estado_anterior = True
        if self.estado_atual is None:
            self.estado_atual = False
        super(Atuador_troca_estado, self).save()


class Atuador_boolean(Task):
    estado = models.NullBooleanField()
    atuador = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, null=True)


class If_else_sensor_string(Task):
    Condicao = [
        (0, '='),
        (1, '!=')
    ]
    condicao = models.IntegerField(choices=Condicao)
    valor = models.CharField(max_length=200)
    elsetask = models.ForeignKey(Task, on_delete=models.CASCADE,
                                      related_name='elsetasksensor_string', null=True)


class If_else_sensor_numero(Task):
    Condicao = [
        (0, '='),
        (1, '!='),
        (2, '>'),
        (3, '>='),
        (4, '<'),
        (5, '<=')
    ]
    condicao = models.IntegerField(choices=Condicao)
    valor = models.IntegerField()
    elsetask = models.ForeignKey(Task, on_delete=models.CASCADE,
                                 related_name='elsetasksensor_numero', null=True)


class If_else_sensor_dadosensor(Task):
    Condicao = [
        (0, '='),
        (1, '!='),
        (2, '>'),
        (3, '>='),
        (4, '<'),
        (5, '<=')
    ]
    condicao = models.IntegerField(choices=Condicao)
    valor = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='If_else_sensor_dadosensor')
    elsetask = models.ForeignKey(Task, on_delete=models.CASCADE,
                                 related_name='elsetasksensor_dadosensor', null=True)


class If_else_sensor_boolean(Task):
    Condicao = [
        (0, '='),
        (1, '!=')
    ]
    condicao = models.IntegerField(choices=Condicao)
    valor = models.NullBooleanField()
    elsetask = models.ForeignKey(Task, on_delete=models.CASCADE,
                                 related_name='elsetasksensor_boolean', null=True)
