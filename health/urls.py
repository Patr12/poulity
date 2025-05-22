app_name = 'finance'  # au jina la app husika

from django.urls import path
from . import views

urlpatterns = [
    path('diseases/', views.disease_list, name='disease_list'),
    path('diseases/<int:pk>/', views.disease_detail, name='disease_detail'),

    path('vaccines/', views.vaccination_list, name='vaccination_list'),
    path('vaccination-records/', views.vaccination_records, name='vaccination_records'),

    path('mortalities/', views.mortality_list, name='mortality_list'),
    path('water-usages/', views.water_usage_list, name='water_usage_list'),

    path('health-status/', views.health_status_list, name='health_status_list'),
    path('environment/', views.environment_logs, name='environment_logs'),
    path('nutrition/', views.nutrition_logs, name='nutrition_logs'),

    # path('', views.customer_view, name='customer_list'),
]
