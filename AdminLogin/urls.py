from django.contrib import admin
from django.urls import path,include
from . import views
app_name="adminlogin"

urlpatterns=[
    path('',views.upload,name="index")
]