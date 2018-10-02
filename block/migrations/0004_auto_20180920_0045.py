# Generated by Django 2.0.5 on 2018-09-20 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0003_proxy_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proxy',
            name='status',
            field=models.IntegerField(choices=[(0, 'Conectando'), (1, 'Conectado'), (2, 'ERRO'), (3, 'Parado'), (4, 'Não Existe')], default=3),
        ),
    ]