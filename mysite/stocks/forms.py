from django import forms

class TickForm(forms.Form):
    Ticker = forms.CharField(label='Ticker ',max_length=6)

