from django import forms


class UploadFileForm(forms.Form):
	
	file = forms.FileField(widget=forms.FileInput(attrs={'class' : 'form-control btn btn-outline-secondary','style':'height:45px'}))
    