# Generated by Django 2.0.5 on 2018-09-30 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tarefa', '0002_auto_20180930_1343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='atuador',
            name='proxy',
        ),
        migrations.RemoveField(
            model_name='sensor',
            name='proxy',
        ),
    ]
