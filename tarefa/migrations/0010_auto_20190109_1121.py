# Generated by Django 2.1.4 on 2019-01-09 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarefa', '0009_auto_20190104_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dado',
            name='valor_char',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='dado',
            name='valor_int',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
