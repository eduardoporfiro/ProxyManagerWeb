# Generated by Django 2.0.5 on 2018-10-21 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarefa', '0014_auto_20181020_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='dado',
            name='proxy_alt_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='dispositivo',
            name='proxy_alt_id',
            field=models.IntegerField(null=True),
        ),
    ]