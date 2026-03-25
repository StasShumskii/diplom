from datetime import datetime

from cars.models import UserCar
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from services.models import Service

from .models import Booking


@login_required
def booking_list(request):
    bookings = Booking.objects.filter(client=request.user).order_by("-scheduled_at")
    return render(request, "bookings/list.html", {"bookings": bookings})


@login_required
def booking_create(request):
    today = datetime.now().strftime("%Y-%m-%d")
    hours_list = ["08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18"]

    service_id = request.GET.get("service")
    selected_service = None
    service_filter = None

    if service_id:
        try:
            selected_service = Service.objects.get(id=service_id)
            service_filter = selected_service.name
        except Service.DoesNotExist:
            pass

    booked_dates = []
    bookings_query = Booking.objects.all()
    if service_filter:
        bookings_query = bookings_query.filter(service_type=service_filter)

    for booking in bookings_query:
        booked_dates.append(
            {
                "date": booking.scheduled_at.strftime("%Y-%m-%d"),
                "hour": booking.scheduled_at.strftime("%H"),
                "status": booking.status,
            }
        )

    booked_dates_json = str(booked_dates).replace("'", '"')

    if request.method == "POST":
        car_id = request.POST.get("car")
        scheduled_date = request.POST.get("scheduled_at", "")
        selected_time = request.POST.get("selected_time", "")
        notes = request.POST.get("notes", "")

        if not car_id:
            return render(
                request,
                "bookings/create.html",
                {
                    "cars": UserCar.objects.filter(user=request.user),
                    "hours_list": hours_list,
                    "today": today,
                    "booked_dates_json": booked_dates_json,
                    "selected_service": selected_service,
                    "error": "Виберіть автомобіль",
                },
            )

        try:
            car = UserCar.objects.get(id=car_id, user=request.user)
        except UserCar.DoesNotExist:
            return render(
                request,
                "bookings/create.html",
                {
                    "cars": UserCar.objects.filter(user=request.user),
                    "hours_list": hours_list,
                    "today": today,
                    "booked_dates_json": booked_dates_json,
                    "selected_service": selected_service,
                    "error": "Автомобіль не знайдено",
                },
            )

        if scheduled_date and selected_time:
            try:
                date_str = f"{scheduled_date} {selected_time}:00"
                scheduled_at = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                from django.utils import timezone

                scheduled_at = timezone.make_aware(scheduled_at)
            except ValueError:
                from django.utils import timezone

                scheduled_at = timezone.now()
        else:
            from django.utils import timezone

            scheduled_at = timezone.now()

        service_type = request.POST.get("service_type", "")

        booking = Booking.objects.create(
            client=request.user,
            car=car,
            scheduled_at=scheduled_at,
            service_type=service_type,
            notes=notes,
            status="PENDING",
        )

        return redirect("bookings:list")

    cars = UserCar.objects.filter(user=request.user)
    return render(
        request,
        "bookings/create.html",
        {
            "cars": cars,
            "hours_list": hours_list,
            "today": today,
            "booked_dates_json": booked_dates_json,
            "selected_service": selected_service,
        },
    )
