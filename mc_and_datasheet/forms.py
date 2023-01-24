from django import forms

class CreateNewSection(forms.Form):

    name = forms.CharField(label=" Section Title", max_length=200)
    check = forms.BooleanField()



