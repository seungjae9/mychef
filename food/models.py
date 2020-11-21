from django.db import models

# Create your models here.
class Food(models.Model):
    name = models.CharField(max_length=100)
    reci = models.CharField(max_length=500)
    cookingOrder = models.CharField(max_length=500)
    image = models.CharField(max_length=500)