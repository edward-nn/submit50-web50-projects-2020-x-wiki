from django import forms

class NewEntryForm(forms.Form):
    new_title = forms.CharField(label="Entry title")
    new_body = forms.CharField(widget=forms.Textarea, label='')

class EditEntryForm(forms.Form):
    edit_body = forms.CharField(widget=forms.Textarea,label='')
