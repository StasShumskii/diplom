from django.urls import path

from . import views

app_name = "notifications"

urlpatterns = [
    path("", views.notification_list, name="list"),
    path("mark-read/<int:pk>/", views.mark_notification_read, name="mark_read"),
    path("reviews/", views.reviews_list, name="reviews"),
    path("add-review/", views.add_review, name="add_review"),
]
