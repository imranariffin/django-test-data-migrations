from django.db import models



class Animal(models.Model):
    species = models.CharField(null=False, blank=False)
    name = models.CharField(null=False, blank=False)
