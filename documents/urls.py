# au jina la app husika

from django.urls import path
from . import views
app_name = 'documents'  
urlpatterns = [
    path('document_list/', views.document_list, name='document_list'),
    path('upload/', views.upload_document, name='upload_document'),
    path('<int:pk>/', views.document_detail, name='document_detail'),
    # path('', views.customer_view, name='customer_list'),
]
