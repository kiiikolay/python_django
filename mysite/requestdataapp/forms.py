from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile

class UserBioForm(forms.Form):
    name = forms.CharField(label="Имя", max_length=100)
    age = forms.IntegerField(label="Возраст", min_value=1, max_value=120)
    bio = forms.CharField(label="Биография", widget=forms.Textarea)

def validate_file_name(file: InMemoryUploadedFile) -> None:
    if file.name and "virus" in file.name:
        raise ValidationError("Имя файла не должно содержать 'Вирус'")

class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_name])