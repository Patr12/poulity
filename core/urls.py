from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),   
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('feeding/', views.feeding, name='feeding'),
    path('order/', views.order, name='order'),
    path('health_dashboard/', views.health_dashboard, name='health_dashboard'),
    path('report/', views.report, name='report'),
    path('settings/', views.settings, name='settings'),
    path('Calenda/', views.calenda, name='calenda'),
    path('chicken/', views.chicken_view, name='chicken'),
    path('eggproduction/', views.egg_production_view, name='eggproduction'),
    path('incubation/', views.incubation_view, name='incubation'),
    path('chickgrowth/', views.chick_growth_view, name='chickgrowth'),
    path('customer/', views.customer_view, name='customer'),
    
]


