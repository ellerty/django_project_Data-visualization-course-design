# visualization/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.map_view, name='map_view'),  # 根路径显示地图
]
