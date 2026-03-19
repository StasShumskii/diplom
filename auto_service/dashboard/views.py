from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from bookings.models import Booking, ServiceHistory, BonusPoints, BonusTransaction
from notifications.models import Review, ChatMessage, Reminder, Notification, UserProposal
from cars.models import UserCar
from django.db.models import Sum
from datetime import datetime, timedelta


def home(request):
    return render(request, 'public/home.html')


def contacts_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        phone = request.POST.get('phone', '').strip()
        
        if name and email and subject and message:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            user_instance = None
            if request.user.is_authenticated:
                user_instance = request.user
            
            proposal = UserProposal.objects.create(
                user=user_instance,
                subject=subject,
                message=f"Від: {name}\nEmail: {email}\nТелефон: {phone or 'Не вказано'}\n\nПовідомлення:\n{message}",
                phone=phone
            )
            
            managers = User.objects.filter(role='MANAGER')
            for manager in managers:
                Notification.objects.create(
                    user=manager,
                    title=f'Нова пропозиція від {name}',
                    message=f'{subject}: {message[:100]}...'
                )
            
            return render(request, 'public/contacts.html', {'success': True})
        else:
            return render(request, 'public/contacts.html', {'error': 'Заповніть всі поля'})
    
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
            context['bookings'] = Booking.objects.filter(client=user).order_by('-scheduled_at')[:10]
            context['cars'] = UserCar.objects.filter(user=user)
            context['bonus_account'], _ = BonusPoints.objects.get_or_create(user=user)
            context['bonus_transactions'] = BonusTransaction.objects.filter(user=user).order_by('-created_at')[:10]
            context['service_history'] = ServiceHistory.objects.filter(car__user=user).order_by('-service_date')[:10]
            context['reminders'] = Reminder.objects.filter(user=user, is_active=True)[:5]
            context['unread_notifications'] = Notification.objects.filter(user=user, is_read=False).count()
            context['my_reviews'] = Review.objects.filter(user=user).order_by('-created_at')[:5]
        
        elif user.role == 'MANAGER':
            context['total_bookings'] = Booking.objects.count()
            context['revenue'] = Booking.objects.filter(status='DONE').aggregate(Sum('total_cost'))['total_cost__sum'] or 0
            context['recent_bookings'] = Booking.objects.all().order_by('-created_at')[:10]
            context['pending_bookings'] = Booking.objects.filter(status='PENDING').count()
            context['all_reviews'] = Review.objects.all().order_by('-created_at')[:20]
            context['pending_reviews_count'] = Review.objects.filter(is_approved=False).count()
            context['proposals'] = UserProposal.objects.all().order_by('-created_at')[:20]
            context['proposals_count'] = UserProposal.objects.filter(is_read=False).count()
            
            total_slots_today = 20
            booked_slots_today = Booking.objects.filter(
                scheduled_at__date=datetime.now().date(),
                status__in=['PENDING', 'CONFIRMED', 'IN_PROGRESS']
            ).count()
            context['shop_load'] = min(int((booked_slots_today / total_slots_today) * 100), 100)
            context['booked_slots'] = booked_slots_today
            context['total_slots'] = total_slots_today
            
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
    from cars.models import CarBrand
    bookings = Booking.objects.filter(client=request.user).order_by('-scheduled_at')[:10]
    cars = UserCar.objects.filter(user=request.user)
    bonus_account, _ = BonusPoints.objects.get_or_create(user=request.user)
    bonus_transactions = BonusTransaction.objects.filter(user=request.user).order_by('-created_at')[:10]
    brands = CarBrand.objects.all()
    
    return render(request, 'account/profile.html', {
        'bookings': bookings,
        'cars': cars,
        'bonus_account': bonus_account,
        'bonus_transactions': bonus_transactions,
        'brands': brands
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


@login_required
def proposals_view(request):
    if request.user.role not in ['MANAGER', 'ADMIN']:
        return redirect('dashboard:index')
    
    proposals = UserProposal.objects.all().order_by('-created_at')
    return render(request, 'dashboard/proposals.html', {'proposals': proposals})


@login_required
@require_POST
def mark_proposal_read(request, proposal_id):
    if request.user.role not in ['MANAGER', 'ADMIN']:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
    
    proposal = get_object_or_404(UserProposal, id=proposal_id)
    proposal.is_read = True
    proposal.save()
    return JsonResponse({'status': 'success'})


@login_required
@require_POST
def mark_proposal_processed(request, proposal_id):
    if request.user.role not in ['MANAGER', 'ADMIN']:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
    
    proposal = get_object_or_404(UserProposal, id=proposal_id)
    proposal.is_processed = True
    proposal.is_read = True
    proposal.save()
    return JsonResponse({'status': 'success'})


@login_required
def get_proposals_count(request):
    if request.user.role not in ['MANAGER', 'ADMIN']:
        return JsonResponse({'count': 0})
    
    count = UserProposal.objects.filter(is_read=False).count()
    return JsonResponse({'count': count})


@login_required
def get_proposals_list(request):
    if request.user.role not in ['MANAGER', 'ADMIN']:
        return JsonResponse({'proposals': []})
    
    proposals = UserProposal.objects.filter(is_read=False).order_by('-created_at')[:10].values(
        'id', 'subject', 'message', 'phone', 'created_at', 'user__email'
    )
    return JsonResponse({'proposals': list(proposals)})


@login_required
def manage_users_view(request):
    if request.user.role not in ['MANAGER', 'ADMIN']:
        return redirect('dashboard:index')
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'dashboard/manage_users.html', {'users': users})


@login_required
@require_POST
def create_user_view(request):
    if request.user.role not in ['MANAGER', 'ADMIN']:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    email = request.POST.get('email', '').strip()
    first_name = request.POST.get('first_name', '').strip()
    last_name = request.POST.get('last_name', '').strip()
    phone = request.POST.get('phone', '').strip()
    role = request.POST.get('role', 'CLIENT')
    password = request.POST.get('password', '').strip()
    
    if not email or not password:
        return JsonResponse({'status': 'error', 'message': 'Email та пароль обов\'язкові'})
    
    if User.objects.filter(email=email).exists():
        return JsonResponse({'status': 'error', 'message': 'Користувач з таким email вже існує'})
    
    try:
        username = email.split('@')[0]
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{email.split('@')[0]}{counter}"
            counter += 1
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role=role
        )
        
        return JsonResponse({'status': 'success', 'message': f'Користувач {email} створений успішно!'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_required
@require_POST
def toggle_user_status(request, user_id):
    if request.user.role not in ['MANAGER', 'ADMIN']:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    target_user = get_object_or_404(User, id=user_id)
    
    if target_user == request.user:
        return JsonResponse({'status': 'error', 'message': 'Неможливо змінити свій власний акаунт'})
    
    target_user.is_active = not target_user.is_active
    target_user.save()
    
    status = 'активовано' if target_user.is_active else 'деактивовано'
    return JsonResponse({'status': 'success', 'message': f'Користувач {status}'})
