from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, HttpResponse
from django import forms
from Outrights.models import *
from Outrights.views import Helper
import  re

class UploadFileForm(forms.Form):
    market_choices = [('Euribor', 'Euribor'), ('Sterling', 'Sterling'), ('EuroSwiss', 'EuroSwiss'),\
                      ('Robusta','Robusta'),('Cocoa','Cocoa'),('WhiteSugar','WhiteSugar'),\
                      ('MillingWheat','MillingWheat'),('RapeSeed','RapeSeed')]
    database=forms.CharField(label="Select market",widget=forms.Select(choices=market_choices))
    file = forms.FileField(label="Choose File")

def upload(request):
    helper=Helper()
    check_admin=helper.isadmin(request)
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                market_model = {'Euribor': EuriborData, 'Sterling': SterlingData, 'EuroSwiss': EuroSwissData, \
                                'Robusta': RobustaData, 'Cocoa': CocoaData, 'WhiteSugar': WhiteSugarData, \
                                'MillingWheat': MillingWheatData, 'RapeSeed': RapeSeedData}
                model=market_model[request.POST['database']]
                model.objects.all().delete()

                request.FILES['file'].save_to_database(
                    model=model,
                    mapdict=['date']+["contract"+str(i) for i in range(180)]
                )



                return render(request,'AdminLogin/upload_form.html',context={'form':form,'admin':check_admin,'confirm':True})
            except Exception as e:
                print(e)
                return render(request,'AdminLogin/upload_form.html',context={'form':form,'admin':check_admin,'error':True})
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(request,'AdminLogin/upload_form.html',context={'form':form,'admin':check_admin})