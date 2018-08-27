# Generated by Django 2.0.5 on 2018-08-27 00:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Broker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endereco', models.CharField(max_length=200)),
                ('porta', models.IntegerField(default=1883)),
                ('username', models.CharField(blank=True, max_length=200)),
                ('password', models.CharField(blank=True, max_length=200)),
                ('estado', models.IntegerField(choices=[(0, 'Desligado'), (1, 'Iniciando'), (2, 'Rodando'), (3, 'Com Problemas'), (4, 'Não Conectado'), (5, 'Parando')], default=0)),
                ('name', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Dado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('QoS', models.IntegerField(choices=[(0, 'QoS - 0'), (1, 'QoS - 1'), (2, 'QoS - 2')], default=0, editable=False)),
                ('dado', models.CharField(editable=False, max_length=200)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Mqtt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topico', models.CharField(max_length=250)),
                ('QoS', models.IntegerField(choices=[(0, 'QoS - 0'), (1, 'QoS - 1'), (2, 'QoS - 2')], default=0)),
                ('RC', models.IntegerField(choices=[(0, 'Conexão Aceita'), (1, 'Conexão Recusada, Versão de Protocolo não aceita'), (2, 'Conexão Recusada, identificador recusado'), (3, 'Conexão Recusada, servidor indisponível'), (4, 'Conexão Recusada, Usuário ou Senha inválido'), (5, 'Conexão Recusada, conexão não autorizada')], default=0)),
                ('broker', models.ForeignKey(on_delete=True, related_name='mqtt', to='block.Broker')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Proxy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('url', models.CharField(max_length=150)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='mqtt',
            name='proxy',
            field=models.ForeignKey(blank=True, on_delete=True, related_name='mqtt', to='block.Proxy'),
        ),
        migrations.AddField(
            model_name='dado',
            name='mqtt',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='dado', to='block.Mqtt'),
        ),
        migrations.AddField(
            model_name='broker',
            name='proxy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proxy_set', to='block.Proxy'),
        ),
    ]
