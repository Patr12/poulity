app_name = 'health'  # au jina la app husika

from django.urls import path
from . import views

urlpatterns = [
    path('diseases/', views.disease_list, name='disease_list'),
    path('diseases/<int:pk>/', views.disease_detail, name='disease_detail'),

    path('vaccines/', views.vaccination_list, name='vaccination_list'),
    path('vaccination-records/', views.vaccination_records, name='vaccination_records'),

    path('mortalities/', views.mortality_list, name='mortality_list'),
    path('water-usages/', views.water_usage_list, name='water_usage_list'),
      # Routes za HealthStatus

    path('health-status/add/', views.add_health_status, name='add_health'),
    path('health-status/edit/<int:pk>/', views.edit_health_status, name='edit_health'),
    path('health-status/delete/<int:pk>/', views.delete_health_status, name='delete_health'),
    path('health-status/', views.health_status_list, name='health_status_list'),
    path('environment/', views.environment_logs, name='environment_logs'),
    path('nutrition/', views.nutrition_logs, name='nutrition_logs'),

    # path('', views.customer_view, name='customer_list'),
    path('feeding/add/', views.add_feeding, name='add_feeding'),
    path('feeding/edit/<int:pk>/', views.edit_feeding, name='edit_feeding'),
    path('feeding/delete/<int:pk>/', views.delete_feeding, name='delete_feeding'),
    path('chicken/<int:pk>/', views.chicken_detail, name='chicken_detail'),
]
