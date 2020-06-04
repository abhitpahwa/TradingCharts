from django import forms
import re
from django.core.exceptions import ValidationError

outright_choices=[(' ',''),('h10','H10'),('m10','M10'),('u10','U10'),('z10','Z10'),
                  ('h11','H11'),('m11','M11'),('u11','U11'),('z11','Z11'),
                  ('h12','H12'),('m12','M12'),('u12','U12'),('z12','Z12'),
                  ('h13','H13'),('m13','M13'),('u13','U13'),('z13','Z13'),
                  ('h14','H14'),('m14','M14'),('u14','U14'),('z14','Z14'),
                  ('h15','H15'),('m15','M15'),('u15','U15'),('z15','Z15'),
                  ('h16','H16'),('m16','M16'),('u16','U16'),('z16','Z16'),
                  ('h17','H17'),('m17','M17'),('u17','U17'),('z17','Z17'),
                  ('h18','H18'),('m18','M18'),('u18','U18'),('z18','Z18'),
                  ('h19','H19'),('m19','M19'),('u19','U19'),('z19','Z19'),
                  ]

class OutrightsForm(forms.Form):
    outright1 = forms.CharField(label="Choose Outright1",widget=forms.Select(choices=outright_choices))
    outright2 = forms.CharField(label="Choose Outright2", widget=forms.Select(choices=outright_choices))
    outright3 = forms.CharField(label="Choose Outright3", widget=forms.Select(choices=outright_choices))
    outright4 = forms.CharField(label="Choose Outright4", widget=forms.Select(choices=outright_choices))
    years=forms.IntegerField(max_value=4,min_value=1,required=True)

class SpreadsForm(forms.Form):
    outright1=forms.CharField(label="Choose Spread1",widget=forms.Select(choices=outright_choices))
    outright2=forms.CharField(widget=forms.Select(choices=outright_choices))
    outright3 = forms.CharField(label="Choose Spread2", widget=forms.Select(choices=outright_choices))
    outright4 = forms.CharField(widget=forms.Select(choices=outright_choices))
    outright5 = forms.CharField(label="Choose Spread3", widget=forms.Select(choices=outright_choices))
    outright6 = forms.CharField(widget=forms.Select(choices=outright_choices))
    outright7 = forms.CharField(label="Choose Spread4", widget=forms.Select(choices=outright_choices))
    outright8 = forms.CharField(widget=forms.Select(choices=outright_choices))
    years = forms.IntegerField(max_value=4, min_value=1,required=True)

class FlysForm(forms.Form):
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
    years = forms.IntegerField(max_value=4, min_value=1,required=True)

class CustomForm(forms.Form):
    expression=forms.CharField(label="Enter the equation to be evaluated",max_length=50)
    years=forms.IntegerField(max_value=4,min_value=1,required=True)
    print("1")
    def clean_expression(self):
        print("2")
        expr=self.cleaned_data['expression']
        pattern=r"^[+-]{0,1}[\d]*[a-zA-Z][0-9]{2}([+-][\d]*[a-zA-Z][0-9]{2})*$"
        if re.match(pattern,expr):
            print("3")
            return expr
        else:
            print("4")
            raise forms.ValidationError("enter a valid expression")
