from django import forms
from tours.models import Tour

class CreateTourForm(forms.ModelForm):

    class Meta:
        """docstring for [object Object]."""
        model = Tour
        exclude = ('Exclusions',)




class SearchTourForm(forms.Form):
    Country = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Type = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control','placeholder':'Type of tour'}))
    Destination = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    StartDate = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker form-control'}))
