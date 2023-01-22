from django import forms

class CreateNewSection(forms.Form):

    name = forms.CharField(label=" Model name ", max_length=500)
    check = forms.BooleanField()



