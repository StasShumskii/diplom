from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from services.models import Service
from cars.models import UserCar

class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Очікує')
        CONFIRMED = 'CONFIRMED', _('Підтверджено')
        IN_PROGRESS = 'IN_PROGRESS', _('В роботі')
        DONE = 'DONE', _('Виконано')
        CANCELLED = 'CANCELLED', _('Скасовано')

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    car = models.ForeignKey(UserCar, on_delete=models.CASCADE, related_name='bookings')
    mechanic = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        limit_choices_to={'role': 'MECHANIC'},
        related_name='assigned_tasks'
    )
    scheduled_at = models.DateTimeField(verbose_name=_('Заплановано на'))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name=_('Статус'))
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('Загальна вартість'))
    notes = models.TextField(blank=True, verbose_name=_('Примітки'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.client.username}"

    class Meta:
        verbose_name = _('Запис на сервіс')
        verbose_name_plural = _('Записи на сервіс')
        ordering = ['-scheduled_at']

class OrderItem(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='items')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price_at_booking = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Ціна на момент запису'))

    def __str__(self):
        return f"{self.service.name} for Booking #{self.booking.id}"

class Invoice(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='invoice')
    issued_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False, verbose_name=_('Оплачено'))
    pdf_file = models.FileField(upload_to='invoices/', blank=True, null=True)

    def __str__(self):
        return f"Invoice for Booking #{self.booking.id}"


class ServiceHistory(models.Model):
    car = models.ForeignKey(UserCar, on_delete=models.CASCADE, related_name='service_history')
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True, related_name='history_records')
    service_date = models.DateTimeField(verbose_name=_('Дата послуги'))
    service_type = models.CharField(max_length=200, verbose_name=_('Тип послуги'))
    description = models.TextField(verbose_name=_('Опис робіт'))
    mileage_at_service = models.PositiveIntegerField(verbose_name=_('Пробіг на момент ТО'))
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Вартість'))
    warranty_until = models.DateField(blank=True, null=True, verbose_name=_('Гарантія до'))
    mechanic_notes = models.TextField(blank=True, verbose_name=_('Нотатки механіка'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car} - {self.service_type} ({self.service_date})"

    class Meta:
        verbose_name = _('Історія ТО')
        verbose_name_plural = _('Історія ТО')
        ordering = ['-service_date']


class BonusPoints(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bonus_account')
    points = models.PositiveIntegerField(default=0, verbose_name=_('Бали'))
    total_earned = models.PositiveIntegerField(default=0, verbose_name=_('Всього зароблено'))
    total_spent = models.PositiveIntegerField(default=0, verbose_name=_('Всього витрачено'))
    level = models.PositiveIntegerField(default=1, verbose_name=_('Рівень'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.points} балів"

    def add_points(self, amount, reason=''):
        self.points += amount
        self.total_earned += amount
        self.level = min(self.total_earned // 5000 + 1, 10)
        self.save()
        BonusTransaction.objects.create(
            user=self.user,
            points=amount,
            transaction_type='EARN',
            description=reason
        )

    def spend_points(self, amount):
        if self.points >= amount:
            self.points -= amount
            self.total_spent += amount
            self.save()
            BonusTransaction.objects.create(
                user=self.user,
                points=amount,
                transaction_type='SPEND',
                description='Витрачено на знижку'
            )
            return True
        return False

    class Meta:
        verbose_name = _('Бонусний рахунок')
        verbose_name_plural = _('Бонусні рахунки')


class BonusTransaction(models.Model):
    class TransactionType(models.TextChoices):
        EARN = 'EARN', _('Зараховано')
        SPEND = 'SPEND', _('Витрачено')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bonus_transactions')
    points = models.IntegerField(verbose_name=_('Кількість балів'))
    transaction_type = models.CharField(max_length=10, choices=TransactionType.choices)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.points} ({self.transaction_type})"

    class Meta:
        verbose_name = _('Бонусна транзакція')
        verbose_name_plural = _('Бонусні транзакції')
        ordering = ['-created_at']
