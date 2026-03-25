from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path("booking/<int:booking_id>/", views.booking_report, name="booking_report"),
    path("analytics/", views.general_analytics_report, name="analytics_report"),
]
