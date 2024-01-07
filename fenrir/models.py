# restaurants/models.py

from django.db import models

class Restaurant(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    access = models.TextField(blank=True, null=True)
    business_hours = models.TextField(blank=True, null=True)
    thumbnail_image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
