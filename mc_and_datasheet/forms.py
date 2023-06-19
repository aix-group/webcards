from django import forms
from .models import Field
from django.core.files.storage import default_storage
    
class FileForm(forms.Form):
    file = forms.FileField(label = 'Select a file')

    def save(self):
        file = self.cleaned_data['file']
        # section_id = self.cleaned_data['section_id']
        # do something with the file, such as saving it to the filesystem or S3
        path = default_storage.save(file.name, file) # Also can be used: path = default_storage.save('path/to/save', file)
        return path

class CreateNewSection(forms.Form):

    name = forms.CharField(label=" Section Title", max_length=200)
    check = forms.BooleanField()


class RadioButtons(forms.Form):
    radiobuttons = forms.BooleanField(widget=forms.RadioSelect)   
    














action="{% url 'mc_and_datasheet:upload_file' section.id %}"