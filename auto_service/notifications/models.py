from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from cars.models import UserCar

class UserProposal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='proposals')
    subject = models.CharField(max_length=255, verbose_name=_('Тема'))
    message = models.TextField(verbose_name=_('Повідомлення'))
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Телефон'))
    is_read = models.BooleanField(default=False, verbose_name=_('Прочитано'))
    is_processed = models.BooleanField(default=False, verbose_name=_('Оброблено'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Proposal from {self.user.email}: {self.subject}"

    class Meta:
        verbose_name = _('Пропозиція користувача')
        verbose_name_plural = _('Пропозиції користувачів')
        ordering = ['-created_at']

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255, verbose_name=_('Заголовок'))
    message = models.TextField(verbose_name=_('Повідомлення'))
    is_read = models.BooleanField(default=False, verbose_name=_('Прочитано'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.title}"

    class Meta:
        verbose_name = _('Сповіщення')
        verbose_name_plural = _('Сповіщення')
        ordering = ['-created_at']


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    car = models.ForeignKey(UserCar, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name=_('Оцінка'))
    title = models.CharField(max_length=200, verbose_name=_('Заголовок'))
    comment = models.TextField(verbose_name=_('Коментар'))
    is_approved = models.BooleanField(default=True, verbose_name=_('Схвалено'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} - {self.rating}/5"

    class Meta:
        verbose_name = _('Відгук')
        verbose_name_plural = _('Відгуки')
        ordering = ['-created_at']


class ChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_messages')
    is_from_admin = models.BooleanField(default=False, verbose_name=_('Від адміністратора'))
    message = models.TextField(verbose_name=_('Повідомлення'))
    is_read = models.BooleanField(default=False, verbose_name=_('Прочитано'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.message[:30]}..."

    class Meta:
        verbose_name = _('Чат повідомлення')
        verbose_name_plural = _('Чат повідомлення')
        ordering = ['created_at']


class Reminder(models.Model):
    class ReminderType(models.TextChoices):
        OIL_CHANGE = 'OIL', _('Заміна оливи')
        TIRE_ROTATION = 'TIRE', _('Ротація шин')
        INSPECTION = 'INSPECTION', _('Техогляд')
        BRAKE_CHECK = 'BRAKE', _('Перевірка гальм')
        AC_SERVICE = 'AC', _('Обслуговування кондиціонера')
        GENERAL = 'GENERAL', _('Загальне ТО')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reminders')
    car = models.ForeignKey(UserCar, on_delete=models.CASCADE, related_name='reminders')
    reminder_type = models.CharField(max_length=20, choices=ReminderType.choices, verbose_name=_('Тип нагадування'))
    title = models.CharField(max_length=200, verbose_name=_('Заголовок'))
    message = models.TextField(verbose_name=_('Повідомлення'))
    reminder_date = models.DateTimeField(verbose_name=_('Дата нагадування'))
    mileage_threshold = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Пробіг для нагадування'))
    is_active = models.BooleanField(default=True, verbose_name=_('Активне'))
    is_sent = models.BooleanField(default=False, verbose_name=_('Відправлено'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reminder for {self.car} - {self.title}"

    class Meta:
        verbose_name = _('Нагадування')
        verbose_name_plural = _('Нагадування')
        ordering = ['reminder_date']
