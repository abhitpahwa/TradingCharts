from django.contrib import admin
from import_export import resources
from .models import EuriborData, SterlingData, EuroSwissData
from import_export.admin import ImportExportModelAdmin
from import_export import fields
from import_export import widgets

cols=['date']
for i in range(180):
    cols.append("contract"+str(i))
cols=tuple(cols)
class EuriborDataResource(resources.ModelResource):
    class Meta:
        model = EuriborData

class EuriborDataAdmin(ImportExportModelAdmin):
    resource_class = EuriborDataResource
    list_display = cols
    list_per_page = 999
    search_fields = ['date']

class SterlingDataResource(resources.ModelResource):
    class Meta:
        model = SterlingData

class SterlingDataAdmin(ImportExportModelAdmin):
    resource_class = SterlingDataResource
    list_display = cols
    list_per_page = 999
    search_fields = ['date']

class EuroSwissDataResource(resources.ModelResource):
    class Meta:
        model = EuroSwissData

class EuroSwissDataAdmin(ImportExportModelAdmin):
    resource_class = EuroSwissDataResource
    list_display = cols
    list_per_page = 999
    search_fields = ['date']

admin.site.register(EuriborData,EuriborDataAdmin)
admin.site.register(SterlingData,SterlingDataAdmin)
admin.site.register(EuroSwissData,EuroSwissDataAdmin)