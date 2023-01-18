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

class Question(models.Model):
    question_text = models.CharField(max_length=200) # This a character field. Search all the fields and have a look what is available.
    pub_date = models.DateTimeField('date published')

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )

    def __str__(self): # Very important to add
        return self.question_text
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0) # A different field you can make use of it.

    def __str__(self):
        return self.answer_text