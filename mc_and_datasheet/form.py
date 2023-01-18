from django.forms import ModelForm
from .models import Question 

# Create the form class.
class QuestionsForm(ModelForm):
    class Meta:
        model = Question
        fields = '__all__'