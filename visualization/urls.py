# visualization/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('data_analysis/',views.data_analysis_view,name='data_analysis'),
    path('api/growth-top-30/', views.growth_top_30, name='growth_top_30'),
    path('api/wealth-top-30/', views.wealth_top_30, name='wealth_top_30'),
    path('api/industry-proportion/', views.industry_proportion, name='industry_proportion'),
    path('character_analysis/', views.character_analysis_view, name='character_analysis'),
    path('character_analysis/<int:pk>/ai-summary/', views.get_ai_summary, name='ai_summary'),
    path('character_analysis/<int:pk>/', views.character_detail_view, name='character_detail'),
    # 其他路由...
]
