# Generated by Django 2.1.2 on 2018-10-23 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarefa', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='settings',
            old_name='url',
            new_name='url_update',
        ),
        migrations.AddField(
            model_name='settings',
            name='url_create',
            field=models.CharField(default='', max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='settings',
            name='task_tipo',
            field=models.IntegerField(choices=[(0, 'save_database'), (1, 'dado_sensor_numero'), (2, 'dado_sensor_string'), (3, 'dados_sensor_media'), (4, 'dado_sensor_min'), (5, 'dado_sensor_max'), (6, 'if_sensor_string'), (7, 'if_sensor_numero'), (8, 'if_sensor_boolean'), (9, 'if_sensor_dadosensor'), (10, 'atuador_troca_estado'), (11, 'atuador_boolean')]),
        ),
    ]