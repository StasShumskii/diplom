from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class CalculationLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    car_brand = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    mileage = models.PositiveIntegerField()
    calculated_price = models.DecimalField(max_digits=12, decimal_places=2)
    ai_recommendations = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Calc {self.id} - {self.car_brand} {self.car_model}"

    class Meta:
        verbose_name = _("Лог розрахунку")
        verbose_name_plural = _("Логи розрахунків")
