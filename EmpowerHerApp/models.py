import re
from django.db import models

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Opportunity(models.Model):
    title=models.CharField(max_length=30)
    lastdate=models.DateField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    description=models.CharField(max_length=900,default='')
    image=models.ImageField()
    applylink=models.CharField(max_length=500)
    isForWomen=models.BooleanField(default=False)
    def __str__(self):
        return self.title

class Person(models.Model):
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=900,default='')
    image=models.ImageField()
    linkedinId=models.CharField(max_length=100)
    twitter=models.CharField(max_length=100)
    def __str__(self):
        return self.name