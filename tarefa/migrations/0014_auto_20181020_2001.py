# Generated by Django 2.0.5 on 2018-10-20 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tarefa', '0013_atuador_boolean'),
    ]

    operations = [
        migrations.RenameField(
            model_name='atuador_boolean',
            old_name='estado_anterior',
            new_name='estado',
        ),
        migrations.RemoveField(
            model_name='atuador_boolean',
            name='estado_atual',
        ),
    ]