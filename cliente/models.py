from django.db import models

# Create your models here.

class Usuarios(models.Model):
    login = models.CharField(max_length=100)
    passwd = models.CharField(max_length=42)

class Recetas(models.Model):
    nombre = models.CharField(max_length=200)
    texto = models.CharField(max_length=200)
    imagen = models.CharField(max_length=200)
    creacion = models.DateTimeField('date published')
    a = models.IntegerField(default=0)
    b = models.IntegerField(default=0)
    c = models.IntegerField(default=0)
    d = models.IntegerField(default=0)
