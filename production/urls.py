  # au jina la app husika

from django.urls import path
from . import views

app_name = 'production'

urlpatterns = [
    path('eggproduction_list/', views.eggproduction_list, name='eggproduction_list'),
    path('eggs/<int:pk>/', views.eggproduction_detail, name='eggproduction_detail'),
    path('eggs/create/', views.eggproduction_create, name='eggproduction_create'),
    path('eggs/<int:pk>/edit/', views.eggproduction_update, name='eggproduction_update'),
    path('eggs/<int:pk>/delete/', views.eggproduction_delete, name='eggproduction_delete'),

    path('incubations/', views.incubation_list, name='incubation_list'),
    path('incubations/<int:pk>/', views.incubation_detail, name='incubation_detail'),
    path('incubations/create/', views.incubation_create, name='incubation_create'),
    path('incubations/<int:pk>/edit/', views.incubation_update, name='incubation_update'),
    path('incubations/<int:pk>/delete/', views.incubation_delete, name='incubation_delete'),

    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
]
    # path('', views.customer_view, name='customer_list'),

