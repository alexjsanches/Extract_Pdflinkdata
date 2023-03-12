from django import forms
from django.forms.widgets import FileInput

class ProcessPDFForm(forms.Form):
    pdf_url = forms.CharField(label='URL do PDF', max_length=200)
    template_path = forms.FileField(label='Template JSON', widget=FileInput)
