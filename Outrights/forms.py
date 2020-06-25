from django import forms
import re
from django.core.exceptions import ValidationError
import datetime

outright_choices=[(' ','' )]
month_codes=['f','g','h','j','k','m','n','q','u','v','x','z']
current_month=datetime.datetime.now().month
current_year=datetime.datetime.now().year-2000
for i in range(180):
    code=month_codes[current_month%12].upper()+str((int)(current_year-10))
    outright_choices.append(('contract'+str(i),code))
    current_month+=1
    if current_month%12==0:
        current_year+=1

market_choices=[('Euribor','Euribor'),('Sterling','Sterling'),('EuroSwiss','EuroSwiss')]

class OutrightsForm(forms.Form):
    market = forms.CharField(label="Choose Market",widget=forms.Select(choices=market_choices))
    outright1 = forms.CharField(label="Choose Outright1",widget=forms.Select(choices=outright_choices))
    outright2 = forms.CharField(label="Choose Outright2", widget=forms.Select(choices=outright_choices))
    outright3 = forms.CharField(label="Choose Outright3", widget=forms.Select(choices=outright_choices))
    outright4 = forms.CharField(label="Choose Outright4", widget=forms.Select(choices=outright_choices))
    years=forms.IntegerField(max_value=5,min_value=1,required=True)

class SpreadsForm(forms.Form):
    market = forms.CharField(label="Choose Market", widget=forms.Select(choices=market_choices))
    outright1=forms.CharField(label="Choose Spread1",widget=forms.Select(choices=outright_choices))
    outright2=forms.CharField(widget=forms.Select(choices=outright_choices))
    outright3 = forms.CharField(label="Choose Spread2", widget=forms.Select(choices=outright_choices))
    outright4 = forms.CharField(widget=forms.Select(choices=outright_choices))
    outright5 = forms.CharField(label="Choose Spread3", widget=forms.Select(choices=outright_choices))
    outright6 = forms.CharField(widget=forms.Select(choices=outright_choices))
    outright7 = forms.CharField(label="Choose Spread4", widget=forms.Select(choices=outright_choices))
    outright8 = forms.CharField(widget=forms.Select(choices=outright_choices))
    years = forms.IntegerField(max_value=5, min_value=1,required=True)

class FlysForm(forms.Form):
    market = forms.CharField(label="Choose Market", widget=forms.Select(choices=market_choices))
    outright1 = forms.CharField(label="Choose Fly1", widget=forms.Select(choices=outright_choices))
    outright2 = forms.CharField(widget=forms.Select(choices=outright_choices))
    outright3 = forms.CharField(widget=forms.Select(choices=outright_choices))
    outright4 = forms.CharField(label="Choose Fly2", widget=forms.Select(choices=outright_choices))
    outright5 = forms.CharField(widget=forms.Select(choices=outright_choices))
    outright6 = forms.CharField(widget=forms.Select(choices=outright_choices))
    outright7 = forms.CharField(label="Choose Fly3", widget=forms.Select(choices=outright_choices))
    outright8 = forms.CharField(widget=forms.Select(choices=outright_choices))
    outright9 = forms.CharField(widget=forms.Select(choices=outright_choices))
    outright10 = forms.CharField(label="Choose Fly4", widget=forms.Select(choices=outright_choices))
    outright11 = forms.CharField(widget=forms.Select(choices=outright_choices))
    outright12 = forms.CharField(widget=forms.Select(choices=outright_choices))
    years = forms.IntegerField(max_value=5, min_value=1,required=True)

class CustomForm(forms.Form):
    market = forms.CharField(label="Choose Market", widget=forms.Select(choices=market_choices))
    expression=forms.CharField(label="Enter the equation to be evaluated",max_length=50)
    years=forms.IntegerField(max_value=5,min_value=1,required=True)
    def clean_expression(self):
        expr=self.cleaned_data['expression']
        pattern=r"^[+-]{0,1}[\d]*[a-zA-Z][0-9]{2}([+-][\d]*[a-zA-Z][0-9]{2})*$"
        if re.match(pattern,expr):
            return expr
        else:
            raise forms.ValidationError("enter a valid expression")
