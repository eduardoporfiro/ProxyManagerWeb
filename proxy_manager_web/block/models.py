from django.db import models

# Create your models here.
class Teste(models.Model):
    sensor = models.CharField(max_length=100)