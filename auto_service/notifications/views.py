from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Notification, Review, ChatMessage, Reminder


@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user)
    notifications.update(is_read=True)
    return render(request, 'notifications/list.html', {'notifications': notifications})


@login_required
@require_POST
def mark_notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'})


def reviews_list(request):
    reviews = Review.objects.filter(is_approved=True).order_by('-created_at')
    return render(request, 'reviews/list.html', {'reviews': reviews})


@login_required
@require_POST
def add_review(request):
    rating = request.POST.get('rating')
    title = request.POST.get('title')
    comment = request.POST.get('comment')
    
    if rating and title and comment:
        Review.objects.create(
            user=request.user,
            rating=rating,
            title=title,
            comment=comment
        )
        
        from bookings.models import BonusPoints
        bonus_account, _ = BonusPoints.objects.get_or_create(user=request.user)
        bonus_account.add_points(50, 'За відгук')
        
        return JsonResponse({'status': 'success', 'message': 'Дякуємо за відгук! Вам нараховано 50 балів!'})
    return JsonResponse({'status': 'error', 'message': 'Заповніть всі поля'})


@login_required
def chat_view(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            ChatMessage.objects.create(user=request.user, message=message, is_from_admin=False)
    
    messages = ChatMessage.objects.filter(user=request.user).order_by('created_at')
    return render(request, 'chat/index.html', {'messages': messages})


@login_required
def get_chat_messages(request):
    messages = ChatMessage.objects.filter(user=request.user).order_by('created_at')
    ChatMessage.objects.filter(user=request.user, is_from_admin=False, is_read=False).update(is_read=True)
    
    data = [{
        'id': m.id,
        'message': m.message,
        'is_from_admin': m.is_from_admin,
        'created_at': m.created_at.strftime('%H:%M')
    } for m in messages]
    
    return JsonResponse({'messages': data})


@login_required
def reminders_list(request):
    reminders = Reminder.objects.filter(user=request.user, is_active=True)
    return render(request, 'reminders/list.html', {'reminders': reminders})


@login_required
@require_POST
def add_reminder(request):
    car_id = request.POST.get('car')
    reminder_type = request.POST.get('reminder_type')
    title = request.POST.get('title')
    message = request.POST.get('message')
    reminder_date = request.POST.get('reminder_date')
    mileage_threshold = request.POST.get('mileage_threshold')
    
    from cars.models import UserCar
    car = get_object_or_404(UserCar, id=car_id, user=request.user)
    
    Reminder.objects.create(
        user=request.user,
        car=car,
        reminder_type=reminder_type,
        title=title,
        message=message,
        reminder_date=reminder_date,
        mileage_threshold=mileage_threshold if mileage_threshold else None
    )
    
    return JsonResponse({'status': 'success', 'message': 'Нагадування створено!'})


@login_required
def delete_reminder(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    reminder.is_active = False
    reminder.save()
    return redirect('reminders:list')
