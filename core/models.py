from django.db import models
from django.utils import timezone

Qos = [
    (0, 'QoS - 0'),
    (1, 'QoS - 1'),
    (2, 'QoS - 2')
]

class AbstractBroker(models.Model):
    ESTADO_BROKER = (
        (0, 'Desligado'),
        (1, 'Iniciando'),
        (2, 'Rodando'),
        (3,'Com Problemas'),
        (4, 'Não Conectado'),
        (5, 'Parando')
    )
    endereco = models.CharField(max_length=200)
    porta = models.IntegerField(default=1883)
    username = models.CharField(max_length=200, blank=True)
    password = models.CharField(max_length=200, blank=True)
    estado = models.IntegerField(choices=ESTADO_BROKER, default=0)
    proxy_alt_id = models.IntegerField(null=True)
    class Meta:
        abstract=True

class AbstractMqtt(models.Model):
    RC = [
        (0,'Conexão Aceita'),
        (1,'Conexão Recusada, Versão de Protocolo não aceita'),
        (2,'Conexão Recusada, identificador recusado'),
        (3, 'Conexão Recusada, servidor indisponível'),
        (4, 'Conexão Recusada, Usuário ou Senha inválido'),
        (5, 'Conexão Recusada, conexão não autorizada'),
    ]
    topico = models.CharField(max_length=250)
    QoS = models.IntegerField(choices=Qos, default=0)
    RC = models.IntegerField(choices=RC, default=0)
    proxy_alt_id = models.IntegerField(null=True)
    class Meta:
        abstract = True

class AbstractDispositivo(models.Model):
    TIPO = (
        (0, 'Atuador'),
        (1, 'Sensor'),
    )
    nome = models.CharField(max_length=200)
    tipo = models.IntegerField(choices=TIPO, default=0)
    is_int = models.BooleanField(default=False)
    proxy_alt_id=models.IntegerField(null=True)
    class Meta:
        abstract=True

class AbstractDado(models.Model):
    QoS = models.IntegerField(default=0, choices=Qos, editable=False)
    valor_char = models.CharField(max_length=500, blank=True)
    valor_int = models.IntegerField(blank=True)
    date = models.DateTimeField(default=timezone.now, editable=False)
    proxy_alt_id = models.IntegerField(null=True)
    class Meta:
        abstract=True

class Celery(models.Model):
    app = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    exception = models.CharField(max_length=200)
    task = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    Tipos = [
        (0, 'save_database'),
        (1, 'dado_sensor_numero'),
        (2, 'dado_sensor_string'),
        (3, 'dados_sensor_media'),
        (4, 'dado_sensor_min'),
        (5, 'dado_sensor_max'),
    ]
    tipo = models.IntegerField(choices=Tipos, null=True)
    comando = models.CharField(max_length=200)
    task_anterior = models.ForeignKey('self', on_delete=models.CASCADE,
                                      related_name='anterior', null=True)
    task_sucessor = models.ForeignKey('self', on_delete=models.CASCADE,
                                      related_name='sucessor', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    proxy_alt_id = models.IntegerField(null=True)
    def __str__(self):
        return self.comando

class If_sensor_string(Task):
    Condicao = [
        (0,'='),
        (1,'!=')
    ]
    condicao = models.IntegerField(choices=Condicao)
    valor = models.CharField(max_length=200, null=True)

class If_sensor_numero(Task):
    Condicao = [
        (0, '='),
        (1, '!='),
        (2,'>'),
        (3,'>='),
        (4,'<'),
        (5,'<=')
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
    valor = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='If_sensor_dadosensor')