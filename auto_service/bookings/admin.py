from django.contrib import admin

from .models import (BonusPoints, BonusTransaction, Booking, Invoice,
                     OrderItem, ServiceHistory)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["id", "client", "car", "scheduled_at", "status", "total_cost"]
    list_filter = ["status", "scheduled_at"]
    search_fields = ["client__username", "car__license_plate"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["booking", "service", "price_at_booking"]


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ["booking", "issued_at", "is_paid"]
    list_filter = ["is_paid"]


@admin.register(ServiceHistory)
class ServiceHistoryAdmin(admin.ModelAdmin):
    list_display = ["car", "service_type", "service_date", "cost"]
    list_filter = ["service_date", "service_type"]
    search_fields = ["car__license_plate", "service_type", "description"]


@admin.register(BonusPoints)
class BonusPointsAdmin(admin.ModelAdmin):
    list_display = ["user", "points", "total_earned", "total_spent", "level"]
    list_filter = ["level"]
    search_fields = ["user__username"]


@admin.register(BonusTransaction)
class BonusTransactionAdmin(admin.ModelAdmin):
    list_display = ["user", "points", "transaction_type", "description", "created_at"]
    list_filter = ["transaction_type", "created_at"]
    search_fields = ["user__username", "description"]
