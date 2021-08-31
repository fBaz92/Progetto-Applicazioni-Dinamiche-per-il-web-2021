from django.db import models
from django.contrib.auth.models import User, AbstractUser
from datetime import date


class Notice(models.Model):
    """Model representing a notice."""
    data_notice = models.DateField()
    data_pubblicazione = models.DateTimeField(null=True, blank=True)
    titolo = models.CharField(max_length=200, null=True, blank=True)
    testo = models.CharField(max_length=20000, null=True, blank=True)
    mittenti = models.CharField(max_length=200, null=True, blank=True)
    
    class Meta:
        ordering = ['data_pubblicazione']

class Lesson(models.Model):
    """Model representing a lesson."""
    data_lesson = models.DateField()
    nome = models.CharField(max_length=300)
    ora_inizio = models.DateTimeField(null=True, blank=True)
    ora_fine = models.DateTimeField(null=True, blank=True)
    id_edificio = models.CharField(max_length=200)
    tipo_luogo = models.CharField(max_length=200)
    nome_luogo = models.CharField(max_length=200)
    
    class Meta:
        ordering = ['nome']


class OfficeHour(models.Model):
    """Model representing a officehour"""
    data_officehour = models.DateField()
    nome = models.CharField(max_length=100)
    note = models.CharField(max_length=2000, null=True, blank=True)
    ora_inizio = models.DateTimeField(null=True, blank=True)
    ora_fine = models.DateTimeField(null=True, blank=True)
    id_edificio = models.CharField(max_length=100)
    tipo_luogo = models.CharField(max_length=100)
    nome_luogo = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['nome']     

class Student(AbstractUser):
      notice = models.ManyToManyField(Notice, help_text='notices selected by a user',)
      lesson = models.ManyToManyField(Lesson, help_text='notices selected by a user',)
      office_hour = models.ManyToManyField(OfficeHour, help_text='notices selected by a user',)
      xxx = models.CharField(max_length=100)

