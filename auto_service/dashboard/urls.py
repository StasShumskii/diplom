from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.MultiRoleDashboardView.as_view(), name='index'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('service-history/', views.service_history_view, name='service_history'),
    path('bonus/', views.bonus_view, name='bonus'),
    path('bonus/spend/', views.spend_bonus, name='spend_bonus'),
    path('reviews/', views.reviews_view, name='reviews'),
    path('contacts/', views.contacts_view, name='contacts'),
]
