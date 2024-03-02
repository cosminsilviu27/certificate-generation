from django import forms

class UploadFileForm(forms.Form):
    file_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    files_data = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control'}))