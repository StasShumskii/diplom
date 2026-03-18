from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from bookings.models import Booking, ServiceHistory, BonusPoints, BonusTransaction
from notifications.models import Review, ChatMessage, Reminder, Notification
from cars.models import UserCar
from django.db.models import Sum
from datetime import datetime, timedelta


def home(request):
    return render(request, 'public/home.html')


def contacts_view(request):
    return render(request, 'public/contacts.html')


class MultiRoleDashboardView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        role = self.request.user.role
        if role == 'MANAGER':
            return ['dashboard/manager.html']
        elif role == 'MECHANIC':
            return ['dashboard/mechanic.html']
        elif role == 'ADMIN':
            return ['dashboard/admin.html']
        return ['dashboard/index.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.role == 'CLIENT':
            context['bookings'] = Booking.objects.filter(client=user).order_by('-scheduled_at')[:5]
            context['cars'] = UserCar.objects.filter(user=user)
            context['bonus_account'], _ = BonusPoints.objects.get_or_create(user=user)
            context['service_history'] = ServiceHistory.objects.filter(car__user=user).order_by('-service_date')[:10]
            context['reminders'] = Reminder.objects.filter(user=user, is_active=True)[:5]
            context['unread_notifications'] = Notification.objects.filter(user=user, is_read=False).count()
        
        elif user.role == 'MANAGER':
            context['total_bookings'] = Booking.objects.count()
            context['revenue'] = Booking.objects.filter(status='DONE').aggregate(Sum('total_cost'))['total_cost__sum'] or 0
            context['recent_bookings'] = Booking.objects.all().order_by('-created_at')[:10]
            context['pending_bookings'] = Booking.objects.filter(status='PENDING').count()
            
        elif user.role == 'MECHANIC':
            context['active_tasks'] = Booking.objects.filter(mechanic=user, status='IN_PROGRESS')

        context['now'] = datetime.now()
        return context


@login_required
def service_history_view(request):
    history = ServiceHistory.objects.filter(car__user=request.user).order_by('-service_date')
    return render(request, 'dashboard/service_history.html', {'history': history})


@login_required
def bonus_view(request):
    bonus_account, _ = BonusPoints.objects.get_or_create(user=request.user)
    transactions = BonusTransaction.objects.filter(user=request.user).order_by('-created_at')[:20]
    
    return render(request, 'dashboard/bonus.html', {
        'bonus_account': bonus_account,
        'transactions': transactions
    })


@login_required
@require_POST
def spend_bonus(request):
    amount = int(request.POST.get('amount', 0))
    bonus_account = get_object_or_404(BonusPoints, user=request.user)
    
    if bonus_account.spend_points(amount):
        return JsonResponse({'status': 'success', 'message': f'{amount} балів витрачено!'})
    return JsonResponse({'status': 'error', 'message': 'Недостатньо балів!'})


@login_required
def reviews_view(request):
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard/reviews.html', {'reviews': reviews})


@login_required
def profile_view(request):
    bookings = Booking.objects.filter(client=request.user).order_by('-scheduled_at')[:10]
    cars = UserCar.objects.filter(user=request.user)
    bonus_account, _ = BonusPoints.objects.get_or_create(user=request.user)
    
    return render(request, 'account/profile.html', {
        'bookings': bookings,
        'cars': cars,
        'bonus_account': bonus_account
    })


@login_required
@require_POST
def update_profile(request):
    user = request.user
    first_name = request.POST.get('first_name', '').strip()
    last_name = request.POST.get('last_name', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()
    
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.phone = phone
    
    try:
        user.save()
        return JsonResponse({
            'success': True,
            'message': 'Профіль оновлено!',
            'avatar_url': user.avatar.url if user.avatar else None
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
