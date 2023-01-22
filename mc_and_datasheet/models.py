from django.db import models
from django.utils import timezone
import datetime
from django.contrib import admin

# Create your models here. 
'''
That small bit of model code gives Django a lot of information. With it, Django is able to:

- Create a database schema (CREATE TABLE statements) for this app.

- Create a Python database-access API for accessing Question and Choice objects.

The three-step guide to making model changes:

- Change your models (in models.py).

- Run python manage.py makemigrations to create migrations for those changes

- Run python manage.py migrate to apply those changes to the database.


'''

class MC_section(models.Model):

    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name
    
class Item(models.Model):
    mc_section = models.ForeignKey(MC_section, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    complete = models.BooleanField()

    def __str__(self):
        return self.text

