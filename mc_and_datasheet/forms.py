from django import forms
from .models import Field
from django.core.files.storage import default_storage
    
class FileForm(forms.Form):
    file = forms.FileField()

    def save(self):
        file = self.cleaned_data['file']
        # do something with the file, such as saving it to the filesystem or S3
        path = default_storage.save(file.name, file) # Also can be used: path = default_storage.save('path/to/save', file)
        return path


class CreateNewSection(forms.Form):

    name = forms.CharField(label=" Section Title", max_length=200)
    check = forms.BooleanField()


class RadioButtons(forms.Form):
    radiobuttons = forms.BooleanField(widget=forms.RadioSelect)   