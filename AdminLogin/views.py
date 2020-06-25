from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, HttpResponse
# from _compact import JsonResponse
from django import forms
from Outrights.models import EuroSwissData,SterlingData,EuriborData
from django.template import RequestContext
import xlrd
from Outrights.views import Helper

class UploadFileForm(forms.Form):
    market_choices = [('Euribor', 'Euribor'), ('Sterling', 'Sterling'), ('EuroSwiss', 'EuroSwiss')]
    database=forms.CharField(label="Select market",widget=forms.Select(choices=market_choices))
    file = forms.FileField(label="Choose File")

def upload(request):
    helper=Helper()
    check_admin=helper.isadmin(request)
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                if request.POST['database']=="Euribor":
                    model=EuriborData
                elif request.POST['database']=="Sterling":
                    model=SterlingData
                elif request.POST['database']=="EuroSwiss":
                    model=EuroSwissData
                model.objects.all().delete()

                request.FILES['file'].save_to_database(
                    model=model,
                    mapdict=['date']+["contract"+str(i) for i in range(180)]
                )
                return render(request,'AdminLogin/upload_form.html',context={'form':form,'admin':check_admin,'confirm':True})
            except Exception as e:
                return render(request,'AdminLogin/upload_form.html',context={'form':form,'admin':check_admin,'error':True})
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(request,'AdminLogin/upload_form.html',context={'form':form,'admin':check_admin})