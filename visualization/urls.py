# visualization/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('data-analysis/',views.data_analysis_view,name='data_analysis'),
    path('api/growth-top-30/', views.growth_top_30, name='growth_top_30'),
    path('api/wealth-top-30/', views.wealth_top_30, name='wealth_top_30'),
    path('api/industry-proportion/', views.industry_proportion, name='industry_proportion'),
    # 其他路由...
]
