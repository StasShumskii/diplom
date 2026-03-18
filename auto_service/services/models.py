from django.db import models
from django.utils.translation import gettext_lazy as _

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Категорія'))
    icon = models.CharField(max_length=50, blank=True, help_text="Lucide icon name")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Категорія послуг')
        verbose_name_plural = _('Категорії послуг')

class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=200, verbose_name=_('Назва послуги'))
    description = models.TextField(blank=True, verbose_name=_('Опис'))
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Базова ціна'))
    estimated_time = models.DurationField(verbose_name=_('Орієнтовний час'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Послуга')
        verbose_name_plural = _('Послуги')

class Part(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Запчастина'))
    code = models.CharField(max_length=50, unique=True, verbose_name=_('Артикул'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Ціна'))
    stock = models.PositiveIntegerField(default=0, verbose_name=_('Кількість на складі'))

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name = _('Запчастина')
        verbose_name_plural = _('Запчастини')
