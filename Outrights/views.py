from django.shortcuts import render
from django.views import generic,View
from .models import Data
from .forms import OutrightsForm,SpreadsForm,FlysForm,CustomForm
from django.http import HttpResponse
from .models import Data
from datetime import datetime, timedelta
import calendar
import re

class Helper():
    def get_day(self,outright):
        month = 0
        year = 0
        month_code = ['h', 'm', 'u', 'z']
        month = 3 * (month_code.index(outright[0]) + 1)
        year = 2000 + int(outright[1:3])
        return datetime(year, month, 1).date()

    def get_expiry(self,curr_date):
        cal = calendar.Calendar(0)
        month = cal.monthdatescalendar(curr_date.year, curr_date.month)
        lastweek = month[-1]
        monday = lastweek[0] - timedelta(days=14)
        return monday

    def get_xaxis(self,length,num_years):
        last_month = num_years * 12
        x_axis = [0] * (length - 1) + [last_month]
        mth = last_month - 1
        ct = 1
        for i in range(length - 2, -1, -1):
            if ct == 21:
                x_axis[i] = mth
                mth -= 1
                ct = 0
            else:
                x_axis[i] = ""
                ct += 1
        return x_axis

    def get_valid_data(self,curr_date,num_years):
        expiry_date = self.get_expiry(curr_date)
        start_date = expiry_date - timedelta(days=365.24 * num_years)
        all_dates = Data.objects.all()
        valid_data = []
        for date_object in all_dates:
            temp_date = datetime.strptime(date_object.date, '%m/%d/%Y').date()
            if temp_date >= start_date and temp_date <= expiry_date:
                valid_data.append(date_object)
        return valid_data

class IndexView(generic.ListView):
    template_name = 'Outrights/index.html'
    context_object_name = 'Options'
    def get_queryset(self):
        return ["Outrights","Spreads","Flys","Customs"]


class OutrightsView(generic.TemplateView):
    helper=Helper()
    def get(self, request):
        form = OutrightsForm()
        return render(request, 'Outrights/ui_outrights.html', {'form': form,'method':'get'})
    def post(self,request):
        form = OutrightsForm(request.POST)
        outrights=[]
        for i in range(4):
            outrights.append(request.POST["outright"+str(i+1)])
        if self.CheckNull(outrights):
            return render(request, 'Outrights/ui_outrights.html',
                          {'form': form,'error':"Enter at least one outright"})
        num_years = float(request.POST['years'])
        legend = []
        y_axis = []
        for o_r in outrights:
            if o_r!=' ':
                y_axis.append(self.get_data_for_outright(num_years,o_r))
                legend.append(o_r.upper())
        x_axis_len=max([len(i) for i in y_axis])
        x_axis = self.helper.get_xaxis(x_axis_len, num_years)
        return render(request, 'Outrights/ui_outrights.html',
                      {'form': form, 'x_axis': x_axis, 'y_axis': y_axis, 'legend': legend,'method':'post'})

    def get_data_for_outright(self,num_years, outright):
        curr_date = self.helper.get_day(outright)
        valid_data = self.helper.get_valid_data(curr_date, num_years)
        y_axis = []
        for object in valid_data:
            if getattr(object, outright):
                y_axis.append(getattr(object, outright))
        return y_axis
    def CheckNull(self,l):
        for i in l:
            if i!=' ':
                return False
        return True

class SpreadsView(generic.TemplateView):
    helper=Helper()
    def get(self, request):
        form = SpreadsForm()
        return render(request, 'Outrights/ui_spreads.html', {'form': form,'method':'get'})
    def post(self,request):
        form = SpreadsForm(request.POST)
        outrights = []
        for i in range(8):
            outrights.append(request.POST["outright" + str(i + 1)])
        if self.CheckNull(outrights):
            return render(request, 'Outrights/ui_spreads.html',
                          {'form': form,'error':"Enter at least one spread"})
        num_years = float(request.POST['years'])
        legend = []
        y_axis = []
        for i in range(0,8,2):
            if outrights[i] != ' ' and outrights[i+1] != ' ':
                y_axis.append(self.get_data_for_spread(num_years, outrights[i], outrights[i+1]))
                legend.append(outrights[i].upper() + "-" + outrights[i+1].upper())
        x_axis_len = max([len(i) for i in y_axis])
        x_axis = self.helper.get_xaxis(x_axis_len, num_years)
        return render(request, 'Outrights/ui_spreads.html',
                      {'form': form, 'x_axis': x_axis, 'y_axis': y_axis, 'legend': legend,'method':'post'})

    def get_data_for_spread(self,num_years,outright1,outright2):
        curr_date=min(self.helper.get_day(outright1),self.helper.get_day(outright2))
        valid_data=self.helper.get_valid_data(curr_date,num_years)
        y_axis=[]
        for object in valid_data:
            if getattr(object, outright1) and getattr(object,outright2):
                y_axis.append(getattr(object, outright1)-getattr(object,outright2))
        return y_axis

    def CheckNull(self,l):
        l=[l[i]+l[i+1] for i in range(0,len(l),2)]
        for i in l:
            if ' ' not in i:
                return False
        return True

class FlysView(generic.TemplateView):
    helper=Helper()
    def get(self,request):
        form = FlysForm()
        return render(request, 'Outrights/ui_flys.html', {'form': form,'method':'get'})
    def post(self,request):
        form = FlysForm(request.POST)
        outrights = []
        for i in range(12):
            outrights.append(request.POST["outright" + str(i + 1)])
        if self.CheckNull(outrights):
            return render(request, 'Outrights/ui_flys.html',
                          {'form': form,'error':"Enter at least one fly"})
        num_years = float(request.POST['years'])
        legend = []
        y_axis = []
        for i in range(0,12,3):
            if outrights[i] != ' ' and outrights[i+1] != ' ' and outrights[i+2] != ' ':
                y_axis.append(self.get_data_for_fly(num_years, outrights[i], outrights[i+1], outrights[i+2]))
                legend.append(outrights[i].upper() + "-" + outrights[i+1].upper() + "-" + outrights[i+2].upper())
        x_axis_len = max([len(i) for i in y_axis])
        x_axis = self.helper.get_xaxis(x_axis_len, num_years)
        return render(request, 'Outrights/ui_flys.html',
                      {'form': form, 'x_axis': x_axis, 'y_axis': y_axis, 'legend': legend,'method':'post'})

    def get_data_for_fly(self,num_years,outright1,outright2,outright3):
        curr_date=min(self.helper.get_day(outright1),self.helper.get_day(outright2),self.helper.get_day(outright3))
        valid_data=self.helper.get_valid_data(curr_date,num_years)
        y_axis=[]
        for object in valid_data:
            if getattr(object, outright1) and getattr(object,outright2) and getattr(object,outright3):
                y_axis.append(getattr(object, outright1)-2*getattr(object,outright2)+getattr(object,outright3))
        return y_axis

    def CheckNull(self,l):
        l=[l[i]+l[i+1]+l[i+2] for i in range(0,len(l),3)]
        for i in l:
            if ' ' not in i:
                return False
        return True

class CustomsView(generic.TemplateView):
    helper=Helper()
    def get(self,request):
        form = CustomForm()
        return render(request, 'Outrights/ui_customs.html', {'form': form,'method':'get'})
    def post(self,request):
        form = CustomForm(request.POST)
        if form.is_valid():
            expr = request.POST['expression'].lower()
            num_years = float(request.POST['years'])
            expr = expr.replace("+", "#+")
            expr = expr.replace("-", "#-")
            if expr[0]!="#":
                expr = "#+" + expr
            print(expr)
            outrights = expr.split("#")
            outrights = [i for i in outrights if i != '']
            print(outrights)
            y_axis = [self.get_data_for_customs(num_years, outrights)]
            x_axis = self.helper.get_xaxis(len(y_axis[0]), num_years)
            legend = [''.join(outrights).upper()]
            return render(request, 'Outrights/ui_customs.html',
                          {'form': form, 'x_axis': x_axis, 'y_axis': y_axis, 'legend': legend,'method':'post'})
        else:
            form=CustomForm()
            return render(request, 'Outrights/ui_customs.html',
                          {'form': form,'error':"Please enter a valid expression"})

    def evaluate(self,expr):
        pattern=r"^([+-])([\d]*)([a-zA-Z])([\d]{2})"
        match=re.match(pattern,expr)
        return [match.group(1),match.group(2),match.group(3)+match.group(4)]

    def get_data_for_customs(self,num_years,outrights):
        outrights_names=[]
        for o_r in outrights:
            index=o_r.find(next(filter(str.isalpha, o_r)))
            outrights_names.append(o_r[index:])
        curr_date=min([self.helper.get_day(i) for i in outrights_names])
        valid_data=self.helper.get_valid_data(curr_date,num_years)
        y_axis=[]
        for object in valid_data:
            check=list(map(lambda x:getattr(object,x),outrights_names))
            y_axis_val=0
            if not (None in check):
                evaluated=list(map(lambda x:self.evaluate(x),outrights))
                for i in evaluated:
                    if i[1]=='':
                        i[1]=1
                    if i[0]=="+":
                        y_axis_val+=getattr(object,i[2])*int(i[1])
                    elif i[0]=="-":
                        y_axis_val -= getattr(object, i[2]) * int(i[1])
                y_axis.append(y_axis_val)
        return y_axis

