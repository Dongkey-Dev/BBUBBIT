from django import forms 

class TickerForm(forms.Form) : 
    ticker = forms.CharField(label = 'Stock Name', max_length=20)