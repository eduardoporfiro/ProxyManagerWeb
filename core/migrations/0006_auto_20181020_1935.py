# Generated by Django 2.0.5 on 2018-10-20 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tarefa', '0011_auto_20181020_1352'),
        ('core', '0005_if_sensor_boolean'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='atuador_troca_estado',
            name='task_ptr',
        ),
        migrations.DeleteModel(
            name='Atuador_troca_estado',
        ),
    ]