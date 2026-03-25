from bookings.models import Booking
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render


@login_required
def booking_report(request, booking_id):
    """
    Professional Print/PDF View for Bookings
    """
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, "reports/invoice_print.html", {"booking": booking})


@login_required
def general_analytics_report(request):
    """
    Manager Analytics Report
    """
    bookings = Booking.objects.all().order_by("-created_at")
    return render(request, "reports/analytics_print.html", {"bookings": bookings})
