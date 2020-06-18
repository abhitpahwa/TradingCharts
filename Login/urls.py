from django.urls import path
from . import views
from django.urls import path,include
app_name='Login'

urlpatterns=[
    path('',views.index_view,name='index')
]