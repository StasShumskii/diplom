from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Booking, OrderItem
from cars.models import UserCar
from services.models import Service

class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(client=self.request.user)

class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    template_name = 'bookings/create.html'
    fields = ['car', 'scheduled_at', 'notes']
    success_url = reverse_lazy('dashboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars'] = UserCar.objects.filter(user=self.request.user)
        context['services'] = Service.objects.all()
        # Pre-select service from URL if present
        service_id = self.request.GET.get('service')
        if service_id:
            context['selected_service'] = get_object_or_404(Service, id=service_id)
        return context

    def form_valid(self, form):
        form.instance.client = self.request.user
        response = super().form_valid(form)
        
        # Handle selected services
        service_ids = self.request.POST.getlist('selected_services')
        total_cost = 0
        for s_id in service_ids:
            service = get_object_or_404(Service, id=s_id)
            OrderItem.objects.create(
                booking=self.object,
                service=service,
                price_at_booking=service.base_price
            )
            total_cost += service.base_price
        
        self.object.total_cost = total_cost
        self.object.save()
        
        return response
