from django import forms
from pyFundamental.utils import sectorList

class addForm(forms.Form):
    symbol = forms.CharField(label='symbol', max_length=100,initial='xxx')

class optionForm(forms.Form):
    sortBy=forms.CharField(label='sortBy', max_length=100,initial='xxx',required=False)
    sector=forms.CharField(label='sector', max_length=100,initial='xxx',required=False)
