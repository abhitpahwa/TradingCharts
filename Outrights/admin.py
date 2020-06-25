from django.contrib import admin
from import_export import resources
from .models import *
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

class RobustaDataResource(resources.ModelResource):
    class Meta:
        model = RobustaData

class RobustaDataAdmin(ImportExportModelAdmin):
    resource_class = RobustaDataResource
    list_display = cols
    list_per_page = 999
    search_fields = ['date']
    
class CocoaDataResource(resources.ModelResource):
    class Meta:
        model = CocoaData

class CocoaDataAdmin(ImportExportModelAdmin):
    resource_class = CocoaDataResource
    list_display = cols
    list_per_page = 999
    search_fields = ['date']
    
class WhiteSugarDataResource(resources.ModelResource):
    class Meta:
        model = WhiteSugarData

class WhiteSugarDataAdmin(ImportExportModelAdmin):
    resource_class = WhiteSugarDataResource
    list_display = cols
    list_per_page = 999
    search_fields = ['date']
    
class MillingWheatDataResource(resources.ModelResource):
    class Meta:
        model = MillingWheatData

class MillingWheatDataAdmin(ImportExportModelAdmin):
    resource_class = MillingWheatDataResource
    list_display = cols
    list_per_page = 999
    search_fields = ['date']
    
class RapeSeedDataResource(resources.ModelResource):
    class Meta:
        model = RapeSeedData

class RapeSeedDataAdmin(ImportExportModelAdmin):
    resource_class = RapeSeedDataResource
    list_display = cols
    list_per_page = 999
    search_fields = ['date']

admin.site.register(EuriborData,EuriborDataAdmin)
admin.site.register(SterlingData,SterlingDataAdmin)
admin.site.register(EuroSwissData,EuroSwissDataAdmin)
admin.site.register(RobustaData,RobustaDataAdmin)
admin.site.register(CocoaData,CocoaDataAdmin)
admin.site.register(WhiteSugarData,WhiteSugarDataAdmin)
admin.site.register(MillingWheatData,MillingWheatDataAdmin)
admin.site.register(RapeSeedData,RapeSeedDataAdmin)

