# reports/urls.py
from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('production/', views.production_report, name='production_report'),
    path('financial/', views.financial_report, name='financial_report'),
    path('health/', views.health_report, name='health_report'),
    path('calendar/events/', views.calendar_events, name='calendar_events'),

     # Routes za HealthReport
    path('reports/', views.report_list, name='report_list'),
    path('reports/add/', views.add_report, name='add_report'),
    path('reports/<int:pk>/', views.view_report, name='view_report'),
    path('reports/edit/<int:pk>/', views.edit_report, name='edit_report'),
    path('reports/delete/<int:pk>/', views.delete_report, name='delete_report'),
]