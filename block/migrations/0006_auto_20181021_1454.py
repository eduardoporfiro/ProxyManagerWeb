# Generated by Django 2.0.5 on 2018-10-21 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0005_auto_20180930_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='broker',
            name='proxy_alt_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='mqtt',
            name='proxy_alt_id',
            field=models.IntegerField(null=True),
        ),
    ]
