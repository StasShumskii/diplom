from django.urls import path
from . import views

app_name = "cars"

urlpatterns = [
    path("", views.car_list, name="list"),
    path("api/models/", views.api_get_models, name="api_models"),
    path("api/add/", views.add_car_ajax, name="add_car_ajax"),
]
