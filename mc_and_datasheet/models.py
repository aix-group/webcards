# Author: Bahadir Eryilmaz 
# Date: 30/09/2023
# Documentation: https://webcards.readthedocs.io/en/latest/index.html
# Desc: This file contains the models of the application. The models are the tables of the database.



from django.db import models
from django.contrib import admin
from django.utils import timezone
from django.contrib.sessions.models import Session
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

###################################### USER INPUT ########################################
class UserInput(models.Model):
    session_uuid = models.CharField(max_length=50, unique=True)
    input_data = models.JSONField()
    session_key = models.ForeignKey(Session, on_delete=models.CASCADE)


########################## MODEL CARD ########################################
class MC_section(models.Model):

    name = models.CharField(max_length=300)
    click_count = models.IntegerField(default=0)
    section_desc = models.CharField(max_length=500, default='')

    mc_section_session = models.CharField(max_length=50, default='',blank=True)

    def givename(self):
        return self.name

    def __str__(self):
        return_text = " %s id: %i" %(self.name, self.id)
        return return_text
    
class Field(models.Model):
    mc_section = models.ForeignKey(MC_section, on_delete=models.CASCADE)
    field_question = models.CharField(max_length=500)
    field_answer = models.TextField(max_length=1000, blank=True)
    field_answer_date = models.DateTimeField(default=timezone.now)
    field_helper = models.CharField(max_length=1000, default='Info about the field', blank=True)
    field_session = models.CharField(max_length=50, default='',blank=True)
   
    def givename(self):
        return str(str(self.id) + '_' + self.field_question)
    
    def __str__(self):
        return "Field question:%s" %(self.field_question)
    
    def get_answer(self):
        return self.field_answer

    
class CardSectionData(models.Model):
    key = models.CharField(max_length=255)
    value = models.JSONField()

    def __str__(self):
       return self.value

class CardData(models.Model):

    card_data = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)
    carddata_session = models.CharField(max_length=50, default='')

    
    def __str__(self):
        return f'{self.card_data}'
    def get(self):
        return f'{self.card_data}'
    
    def extend_dict(self,extension):

        return card_data + extension

class File(models.Model):

    file = models.FileField(upload_to='uploads/')
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_session = models.CharField(max_length=50, default='', null=True)

    uploaded_section_id = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        # Skip saving the file by removing the 'file' attribute temporarily
        file = self.file
        self.file = None
        super().save(*args, **kwargs)
        # Restore the 'file' attribute after saving the file information
        self.file = file

    def givename(self):
        return str(self.name)

    def __str__(self):
        return f'{self.name}, {self.uploaded_at}'

###################################### DATASHEET ##############################

class dt_section(models.Model):

    name = models.CharField(max_length=300)
    section_desc = models.CharField(max_length=500, default='Info about the section')
    dt_section_session = models.CharField(max_length=50, default='',blank=True)

    def givename(self):
        return self.name

    def __str__(self):
        return_text = " %s id: %i" %(self.name, self.id)
        return return_text
    
class dt_Field(models.Model):
    dt_section = models.ForeignKey(dt_section, on_delete=models.CASCADE)
    field_question = models.CharField(max_length=500)
    field_answer = models.TextField(max_length=1000, blank=True)
    field_answer_date = models.DateTimeField(default=timezone.now)
    field_helper = models.CharField(max_length=500, default='Info about the field')
    field_session = models.CharField(max_length=50, default='',blank=True)
   
    def givename(self):

        return str(str(self.id) + '_' + self.field_question)
    
    def __str__(self):
        return "Field question:%s" %(self.field_question)
    
    def get_answer(self):
        return self.field_answer
    
class CardDataDatasheet(models.Model):

    card_data = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)
    carddata_session = models.CharField(max_length=50, default='')
    
    def __str__(self):
        return f'{self.card_data}'
    def get(self):
        return f'{self.card_data}'
    
    def extend_dict(self,extension):

        return card_data + extension

########################### DataCard ############################

class dc_section(models.Model):

    name = models.CharField(max_length=300)

    def givename(self):
        return self.name

    def __str__(self):
        return_text = " %s id: %i" %(self.name, self.id)
        return return_text
    
class dc_Field(models.Model):
    dt_section = models.ForeignKey(dt_section, on_delete=models.CASCADE)
    field_question = models.CharField(max_length=500)
    field_answer = models.TextField(max_length=1000, blank=True)
    field_answer_date = models.DateTimeField(default=timezone.now)
   
    def givename(self):

        return str(str(self.id) + '_' + self.field_question)
    
    def __str__(self):
        return "Field question:%s" %(self.field_question)
    
    def get_answer(self):
        return self.field_answer
    
class CardDataDatacard(models.Model):

    card_data = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.card_data}'
    def get(self):
        return f'{self.card_data}'
    
    def extend_dict(self,extension):

        return card_data + extension
