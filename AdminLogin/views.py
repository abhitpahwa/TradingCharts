from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, HttpResponse
# from _compact import JsonResponse
from django import forms
from Outrights.models import Data,SterlingData
from django.template import RequestContext
import xlrd
from Outrights.views import Helper

class UploadFileForm(forms.Form):
    market_choices = [('Euribor', 'Euribor'), ('Sterling', 'Sterling')]
    database=forms.CharField(label="Select market",widget=forms.Select(choices=market_choices))
    file = forms.FileField(label="Choose File")

def upload(request):
    helper=Helper()
    check_admin=helper.isadmin(request)
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                filehandle = request.FILES['file']
                book=xlrd.open_workbook(file_contents=filehandle.read())
                sheet=book.sheet_by_index(0)
                rows=sheet.nrows
                if request.POST['database']=="Euribor":
                    model=Data
                elif request.POST['database']=="Sterling":
                    model=SterlingData
                model.objects.all().delete()
                for r in range(1,rows):
                    record=model()
                    c=0
                    record.date=sheet.cell_value(r,c)
                    c+=1
                    record.h10 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.m10 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.u10 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.z10 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.h11 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.m11 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.u11 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.z11 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.h12 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.m12 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.u12 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.z12 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.h13 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.m13 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.u13 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.z13 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.h14 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.m14 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.u14 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.z14 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.h15 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.m15 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.u15 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.z15 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.h16 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.m16 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.u16 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.z16 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.h17 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.m17 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.u17 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.z17 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.h18 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.m18 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.u18 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.z18 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.h19 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.m19 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.u19 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    c += 1
                    record.z19 = None if sheet.cell_value(r, c)=='' else sheet.cell_value(r,c)
                    record.save()
                return render(request,'AdminLogin/upload_form.html',context={'form':form,'admin':check_admin,'confirm':True})
            except:
                return render(request,'AdminLogin/upload_form.html',context={'form':form,'admin':check_admin,'error':True})
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(request,'AdminLogin/upload_form.html',context={'form':form,'admin':check_admin})