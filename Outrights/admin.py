from django.contrib import admin
from import_export import resources
from .models import EuriborData, SterlingData, EuroSwissData
from import_export.admin import ImportExportModelAdmin
from import_export import fields
from import_export import widgets

class EuriborDataResource(resources.ModelResource):
    class Meta:
        model = EuriborData

class EuriborDataAdmin(ImportExportModelAdmin):
    resource_class = EuriborDataResource
    list_display = ('date','h10','m10','u10','z10','h11','m11','u11','z11','h12','m12','u12','z12','h13',
                    'm13','u13','z13','h14','m14','u14','z14','h15','m15','u15','z15','h16','m16','u16','z16',
                    'h17','m17','u17','z17','h18','m18','u18','z18','h19','m19','u19','z19')
    list_per_page = 999
    search_fields = ['date']

class SterlingDataResource(resources.ModelResource):
    class Meta:
        model = SterlingData

class SterlingDataAdmin(ImportExportModelAdmin):
    resource_class = SterlingDataResource
    list_display = ('date','h10','m10','u10','z10','h11','m11','u11','z11','h12','m12','u12','z12','h13',
                    'm13','u13','z13','h14','m14','u14','z14','h15','m15','u15','z15','h16','m16','u16','z16',
                    'h17','m17','u17','z17','h18','m18','u18','z18','h19','m19','u19','z19')
    list_per_page = 999
    search_fields = ['date']

class EuroSwissDataResource(resources.ModelResource):
    class Meta:
        model = EuroSwissData

class EuroSwissDataAdmin(ImportExportModelAdmin):
    resource_class = EuroSwissDataResource
    list_display = ('date','h10','m10','u10','z10','h11','m11','u11','z11','h12','m12','u12','z12','h13',
                    'm13','u13','z13','h14','m14','u14','z14','h15','m15','u15','z15','h16','m16','u16','z16',
                    'h17','m17','u17','z17','h18','m18','u18','z18','h19','m19','u19','z19')
    list_per_page = 999
    search_fields = ['date']

admin.site.register(EuriborData,EuriborDataAdmin)
admin.site.register(SterlingData,SterlingDataAdmin)
admin.site.register(EuroSwissData,EuroSwissDataAdmin)