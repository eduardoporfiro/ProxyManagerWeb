# Generated by Django 2.0.5 on 2018-08-26 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proxy',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
