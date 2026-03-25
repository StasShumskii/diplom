from django.contrib import admin

from .models import ChatMessage, Notification, Reminder, Review


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["user", "title", "is_read", "created_at"]
    list_filter = ["is_read", "created_at"]
    search_fields = ["user__username", "title"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "rating", "title", "is_approved", "created_at"]
    list_filter = ["is_approved", "rating", "created_at"]
    search_fields = ["user__username", "title", "comment"]


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ["user", "message", "is_from_admin", "is_read", "created_at"]
    list_filter = ["is_from_admin", "is_read", "created_at"]
    search_fields = ["user__username", "message"]


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "car",
        "reminder_type",
        "title",
        "reminder_date",
        "is_active",
        "is_sent",
    ]
    list_filter = ["reminder_type", "is_active", "is_sent"]
    search_fields = ["user__username", "title"]
