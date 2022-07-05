from django.db import models


class Adjective(models.Model):
    """
    A model to store adjectives and their determiners
    """
    determiner = models.CharField(max_length=5, null=False, blank=False)
    adjective = models.CharField(max_length=120, null=False, blank=False)

    def __str__(self):
        return self.adjective


class Creature(models.Model):
    """
    A model to store creatures, their plural names and their determiners
    """
    determiner = models.CharField(max_length=5, null=False, blank=False)
    creature = models.CharField(max_length=120, null=False, blank=False)
    plural = models.CharField(max_length=120, null=False, blank=False)

    def __str__(self):
        return self.creature


class Activity(models.Model):
    """
    A model to store activities
    """
    class Meta:
        verbose_name_plural = "Activities"

    activity = models.CharField(max_length=120, null=False, blank=False)

    def __str__(self):
        return self.activity


class Location(models.Model):
    """
    A model to store locations
    """
    location = models.CharField(max_length=120, null=False, blank=False)

    def __str__(self):
        return self.location
