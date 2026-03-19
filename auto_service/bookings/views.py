from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime
from .models import Booking
from cars.models import UserCar

@login_required
def booking_list(request):
    bookings = Booking.objects.filter(client=request.user).order_by('-scheduled_at')
    return render(request, 'bookings/list.html', {'bookings': bookings})

@login_required
def booking_create(request):
    today = datetime.now().strftime('%Y-%m-%d')
    hours_list = ['08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18']
    
    if request.method == 'POST':
        car_id = request.POST.get('car')
        scheduled_date = request.POST.get('scheduled_at', '')
        selected_time = request.POST.get('selected_time', '')
        notes = request.POST.get('notes', '')
        
        if not car_id:
            return render(request, 'bookings/create.html', {
                'cars': UserCar.objects.filter(user=request.user),
                'hours_list': hours_list,
                'today': today,
                'error': 'Виберіть автомобіль'
            })
        
        try:
            car = UserCar.objects.get(id=car_id, user=request.user)
        except UserCar.DoesNotExist:
            return render(request, 'bookings/create.html', {
                'cars': UserCar.objects.filter(user=request.user),
                'hours_list': hours_list,
                'today': today,
                'error': 'Автомобіль не знайдено'
            })
        
        if scheduled_date and selected_time:
            try:
                date_str = f"{scheduled_date} {selected_time}:00"
                scheduled_at = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                from django.utils import timezone
                scheduled_at = timezone.make_aware(scheduled_at)
            except ValueError:
                from django.utils import timezone
                scheduled_at = timezone.now()
        else:
            from django.utils import timezone
            scheduled_at = timezone.now()
        
        booking = Booking.objects.create(
            client=request.user,
            car=car,
            scheduled_at=scheduled_at,
            notes=notes,
            status='PENDING'
        )
        
        return redirect('bookings:list')
    
    cars = UserCar.objects.filter(user=request.user)
    return render(request, 'bookings/create.html', {
        'cars': cars,
        'hours_list': hours_list,
        'today': today
    })
