from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.MultiRoleDashboardView.as_view(), name="index"),
    path(
        "booking-status/<int:booking_id>/",
        views.update_booking_status,
        name="update_booking_status",
    ),
    path("booking-assign/<int:booking_id>/", views.assign_mechanic, name="assign_mechanic"),
    # Legacy URLs
    path(
        "dashboard/booking-status/<int:booking_id>/",
        views.update_booking_status,
        name="update_booking_status_legacy",
    ),
    path(
        "dashboard/booking-assign/<int:booking_id>/",
        views.assign_mechanic,
        name="assign_mechanic_legacy",
    ),
    path(
        "dashboard/bookings/<int:booking_id>/status/",
        views.update_booking_status,
        name="update_booking_status_old",
    ),
    path(
        "dashboard/bookings/<int:booking_id>/assign/",
        views.assign_mechanic,
        name="assign_mechanic_old",
    ),
    path("profile/", views.profile_view, name="profile"),
    path("profile/update/", views.update_profile, name="update_profile"),
    path("service-history/", views.service_history_view, name="service_history"),
    path("bonus/", views.bonus_view, name="bonus"),
    path("bonus/spend/", views.spend_bonus, name="spend_bonus"),
    path("reviews/", views.reviews_view, name="reviews"),
    path("contacts/", views.contacts_view, name="contacts"),
    path("proposals/", views.proposals_view, name="proposals"),
    path("proposals/<int:proposal_id>/read/", views.mark_proposal_read, name="proposal_read"),
    path(
        "proposals/<int:proposal_id>/processed/",
        views.mark_proposal_processed,
        name="proposal_processed",
    ),
    path("users/", views.manage_users_view, name="manage_users"),
    path("users/create/", views.create_user_view, name="create_user"),
    path("users/<int:user_id>/toggle/", views.toggle_user_status, name="toggle_user"),
    path("api/proposals/count/", views.get_proposals_count, name="proposals_count"),
    path("api/proposals/list/", views.get_proposals_list, name="proposals_list"),
    path("password-reset/", views.password_reset_view, name="password_reset_view"),
    path("password-reset/do/", views.quick_password_reset, name="quick_password_reset"),
]
