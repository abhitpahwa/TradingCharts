from django.shortcuts import render,redirect
from django.views import generic,View
from .models import Data,SterlingData
from .forms import OutrightsForm,SpreadsForm,FlysForm,CustomForm
from django.http import HttpResponse
from datetime import datetime, timedelta
import calendar
import re
from django.contrib.auth import logout as auth_logout

def logout(request):
    auth_logout(request)
    return redirect("/")

class Helper():
    def isadmin(self,request):
        if request.user.get_username()=="abhit.pahwa":
            return True
        return False
    def check_login(self,request):
        if not request.user.is_authenticated or request.user.is_anonymous:
            return False
        return True
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

    def get_valid_data(self,curr_date,num_years,market):
        expiry_date = self.get_expiry(curr_date)
        start_date = expiry_date - timedelta(days=365.24 * num_years)
        if market=="Euribor":
            all_dates = Data.objects.all()
        elif market=="Sterling":
            all_dates = SterlingData.objects.all()
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

def display_index(request):
    helper=Helper()
    if not helper.check_login(request):
        return redirect("/")
    else:
        return IndexView.as_view()(request)


class OutrightsView(generic.TemplateView):
    helper=Helper()
    def get(self, request):
        if not self.helper.check_login(request): 
            return redirect("/") 
        form = OutrightsForm()
        check_admin=self.helper.isadmin(request)
        return render(request, 'Outrights/ui_outrights.html', {'form': form,'method':'get','admin':check_admin})
    def post(self,request):
        if not self.helper.check_login(request): 
            return redirect("/")
        form = OutrightsForm(request.POST)
        check_admin = self.helper.isadmin(request)
        outrights=[]
        for i in range(4):
            outrights.append(request.POST["outright"+str(i+1)])
        if self.CheckNull(outrights):
            return render(request, 'Outrights/ui_outrights.html',
                          {'form': form,'error':"Enter at least one outright",'admin':check_admin})
        num_years = float(request.POST['years'])
        legend = []
        y_axis = []
        market=request.POST["market"]
        for o_r in outrights:
            if o_r!=' ':
                y_axis.append(self.get_data_for_outright(num_years,o_r,market))
                legend.append(o_r.upper())
        x_axis_len=max([len(i) for i in y_axis])
        x_axis = self.helper.get_xaxis(x_axis_len, num_years)

        return render(request, 'Outrights/ui_outrights.html',
                      {'form': form, 'x_axis': x_axis, 'y_axis': y_axis, 'legend': legend,'method':'post','admin':check_admin})

    def get_data_for_outright(self,num_years,outright,market):
        curr_date = self.helper.get_day(outright)
        valid_data = self.helper.get_valid_data(curr_date, num_years,market)
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
        if not self.helper.check_login(request): 
            return redirect("/")
        form = SpreadsForm()
        check_admin = self.helper.isadmin(request)
        return render(request, 'Outrights/ui_spreads.html', {'form': form,'method':'get','admin':check_admin})
    def post(self,request):
        if not self.helper.check_login(request): 
            return redirect("/")
        form = SpreadsForm(request.POST)
        check_admin = self.helper.isadmin(request)
        outrights = []
        for i in range(8):
            outrights.append(request.POST["outright" + str(i + 1)])
        if self.CheckNull(outrights):
            return render(request, 'Outrights/ui_spreads.html',
                          {'form': form,'error':"Enter at least one spread",'admin':check_admin})
        num_years = float(request.POST['years'])
        legend = []
        y_axis = []
        market = request.POST["market"]
        for i in range(0,8,2):
            if outrights[i] != ' ' and outrights[i+1] != ' ':
                y_axis.append(self.get_data_for_spread(num_years, outrights[i], outrights[i+1],market))
                legend.append(outrights[i].upper() + "-" + outrights[i+1].upper())
        x_axis_len = max([len(i) for i in y_axis])
        x_axis = self.helper.get_xaxis(x_axis_len, num_years)

        return render(request, 'Outrights/ui_spreads.html',
                      {'form': form, 'x_axis': x_axis, 'y_axis': y_axis, 'legend': legend,'method':'post','admin':check_admin})

    def get_data_for_spread(self,num_years,outright1,outright2,market):
        curr_date=min(self.helper.get_day(outright1),self.helper.get_day(outright2))
        valid_data=self.helper.get_valid_data(curr_date,num_years,market)
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
        if not self.helper.check_login(request): 
            return redirect("/")
        form = FlysForm()
        check_admin = self.helper.isadmin(request)
        return render(request, 'Outrights/ui_flys.html', {'form': form,'method':'get','admin':check_admin})
    def post(self,request):
        if not self.helper.check_login(request): 
            return redirect("/")
        form = FlysForm(request.POST)
        outrights = []
        for i in range(12):
            outrights.append(request.POST["outright" + str(i + 1)])
        check_admin = self.helper.isadmin(request)
        if self.CheckNull(outrights):
            return render(request, 'Outrights/ui_flys.html',
                          {'form': form,'error':"Enter at least one fly",'admin':check_admin})
        num_years = float(request.POST['years'])
        legend = []
        y_axis = []
        market = request.POST["market"]
        for i in range(0,12,3):
            if outrights[i] != ' ' and outrights[i+1] != ' ' and outrights[i+2] != ' ':
                y_axis.append(self.get_data_for_fly(num_years, outrights[i], outrights[i+1], outrights[i+2], market))
                legend.append(outrights[i].upper() + "-" + outrights[i+1].upper() + "-" + outrights[i+2].upper())
        x_axis_len = max([len(i) for i in y_axis])
        x_axis = self.helper.get_xaxis(x_axis_len, num_years)

        return render(request, 'Outrights/ui_flys.html',
                      {'form': form, 'x_axis': x_axis, 'y_axis': y_axis, 'legend': legend,'method':'post','admin':check_admin})

    def get_data_for_fly(self,num_years,outright1,outright2,outright3,market):
        curr_date=min(self.helper.get_day(outright1),self.helper.get_day(outright2),self.helper.get_day(outright3))
        valid_data=self.helper.get_valid_data(curr_date,num_years,market)
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
        if not self.helper.check_login(request): 
            return redirect("/")
        form = CustomForm()
        check_admin = self.helper.isadmin(request)
        return render(request, 'Outrights/ui_customs.html', {'form': form,'method':'get','admin':check_admin})
    def post(self,request):
        if not self.helper.check_login(request): 
            return redirect("/")
        form = CustomForm(request.POST)
        if form.is_valid():
            expr = request.POST['expression'].lower()
            num_years = float(request.POST['years'])
            expr = expr.replace("+", "#+")
            expr = expr.replace("-", "#-")
            if expr[0]!="#":
                expr = "#+" + expr
            outrights = expr.split("#")
            outrights = [i for i in outrights if i != '']
            market = request.POST["market"]
            y_axis = [self.get_data_for_customs(num_years, outrights,market)]
            x_axis = self.helper.get_xaxis(len(y_axis[0]), num_years)
            legend = [''.join(outrights).upper()]
            check_admin = self.helper.isadmin(request)
            return render(request, 'Outrights/ui_customs.html',
                          {'form': form, 'x_axis': x_axis, 'y_axis': y_axis, 'legend': legend,'method':'post','admin':check_admin})
        else:
            form=CustomForm()
            check_admin = self.helper.isadmin(request)
            return render(request, 'Outrights/ui_customs.html',
                          {'form': form,'error':"Please enter a valid expression",'admin':check_admin})

    def evaluate(self,expr):
        pattern=r"^([+-])([\d]*)([a-zA-Z])([\d]{2})"
        match=re.match(pattern,expr)
        return [match.group(1),match.group(2),match.group(3)+match.group(4)]

    def get_data_for_customs(self,num_years,outrights,market):
        outrights_names=[]
        for o_r in outrights:
            index=o_r.find(next(filter(str.isalpha, o_r)))
            outrights_names.append(o_r[index:])
        curr_date=min([self.helper.get_day(i) for i in outrights_names])
        valid_data=self.helper.get_valid_data(curr_date,num_years,market)
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

