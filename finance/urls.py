# au jina la app husika

from django.urls import path
from . import views
app_name = 'finance'  

urlpatterns = [
    path('order_list/', views.order_list, name='order_list'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
    path('order/create/', views.create_order, name='create_order'),
    path('order/<int:order_id>/payment/', views.make_payment, name='make_payment'),
    # path('', views.customer_view, name='customer_list'),
]
