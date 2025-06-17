from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'core'

urlpatterns = [
    
    path('', views.home, name='home'),   
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('feeding/', views.feeding, name='feeding'),
    path('order/', views.order, name='order'),
    path('health_dashboard/', views.health_dashboard, name='health_dashboard'),
    path('report/', views.report, name='report'),
    path('settings/', views.settings, name='settings'),
    path('Calenda/', views.calendar_view, name='calenda'),
    path('chicken/', views.chicken_view, name='chicken'),
    path('eggproduction/', views.egg_production_view, name='eggproduction'),
    path('incubation/', views.incubation_view, name='incubation'),
    path('chickgrowth/', views.chick_growth_view, name='chickgrowth'),
    path('customer/', views.customer_view, name='customer'),
    path('add-egg-production/', views.AddEggProductionView.as_view(), name='add_egg_production'),
    path('eggproduction/edit/<int:pk>/', views.edit_egg_production, name='edit_egg_production'),
    path('eggproduction/delete/<int:pk>/', views.delete_egg_production, name='delete_egg_production'),
    #  path ya ku signup na ku signin kwenye  system 
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
     path('profile/', views.profile_view, name='profile'),
     # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('signup/', views.signup_view, name='signup'),

    
]


