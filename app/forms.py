# forms.py
from django import forms

class TextAreaForm(forms.Form):
    text_data = forms.CharField(widget=forms.Textarea, label='Text Data')
