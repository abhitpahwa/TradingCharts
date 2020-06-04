from django.urls import path
from . import views

app_name='Outrights'

urlpatterns=[
    # path('',views.IndexView.as_view(),name='index'),
    path('',views.IndexView.as_view(),name='index_page'),
    # path('outrights/',views.get_outrights,name='Outrights_form'),
    path('outrights/',views.OutrightsView.as_view(),name='Outrights_form'),
    path('spreads/',views.SpreadsView.as_view(),name='Spreads_form'),
    path('flys/',views.FlysView.as_view(),name='Flys_form'),
    path('customs/',views.CustomsView.as_view(),name='Customs_form')
]
