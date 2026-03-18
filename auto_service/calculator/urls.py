from django.urls import path
from . import views

app_name = 'calculator'

urlpatterns = [
    path('', views.CalculatorView.as_view(), name='index'),
    path('api/calculate/', views.api_calculate_estimate, name='estimate'),
    path('api/models/', views.api_get_models, name='api_models'),
]
