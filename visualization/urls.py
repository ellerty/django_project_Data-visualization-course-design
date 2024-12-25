# visualization/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('data-analysis/',views.data_analysis_view,name='data_analysis'),
]
