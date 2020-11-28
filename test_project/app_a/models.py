from django.db import models


class Animal(models.Model):
    species = models.CharField(blank=False, null=False, max_length=50)
    name = models.CharField(blank=False, null=False, max_length=100)

    def __str__(self):
        return f"Animal [name={self.name}, species={self.species}]"
