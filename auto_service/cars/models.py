from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class CarBrand(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Марка"))
    logo = models.ImageField(upload_to="brands/", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Марка авто")
        verbose_name_plural = _("Марки авто")


class CarModel(models.Model):
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=100, verbose_name=_("Модель"))
    year_start = models.PositiveIntegerField(default=2000)
    year_end = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.brand.name} {self.name}"

    class Meta:
        verbose_name = _("Модель авто")
        verbose_name_plural = _("Моделі авто")


class UserCar(models.Model):
    class FuelType(models.TextChoices):
        GASOLINE = "GASOLINE", _("Бензин")
        DIESEL = "DIESEL", _("Дизель")
        LPG = "LPG", _("Газ/Газ-бензин")
        ELECTRIC = "ELECTRIC", _("Електро")
        HYBRID = "HYBRID", _("Гібрид")
        CNG = "CNG", _("Метан")

    class EngineType(models.TextChoices):
        NATURAL = "NATURAL", _("Атмосферний")
        TURBO = "TURBO", _("Турбований")
        SUPERCHARGE = "SUPERCHARGE", _("Наддувний")

    class TechnicalCondition(models.TextChoices):
        EXCELLENT = "EXCELLENT", _("Відмінний")
        GOOD = "GOOD", _("Добрий")
        NEEDS_REPAIR = "NEEDS_REPAIR", _("Потребує ремонту")
        CRITICAL = "CRITICAL", _("Критичний")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="my_cars"
    )
    model = models.ForeignKey(CarModel, on_delete=models.PROTECT)
    vin = models.CharField(
        max_length=17, unique=True, blank=True, null=True, verbose_name=_("VIN-код")
    )
    license_plate = models.CharField(max_length=20, verbose_name=_("Держ. номер"))
    year = models.PositiveIntegerField(verbose_name=_("Рік випуску"))
    mileage = models.PositiveIntegerField(default=0, verbose_name=_("Пробіг (км)"))
    engine_type = models.CharField(
        max_length=20,
        choices=EngineType.choices,
        blank=True,
        null=True,
        verbose_name=_("Тип двигуна"),
    )
    engine_volume = models.DecimalField(
        max_digits=3, decimal_places=1, blank=True, null=True, verbose_name=_("Об'єм двигуна (л)")
    )
    fuel_type = models.CharField(
        max_length=20, choices=FuelType.choices, blank=True, null=True, verbose_name=_("Тип палива")
    )
    technical_condition = models.CharField(
        max_length=20,
        choices=TechnicalCondition.choices,
        default=TechnicalCondition.GOOD,
        verbose_name=_("Технічний стан"),
    )

    def __str__(self):
        return f"{self.model} ({self.license_plate})"

    class Meta:
        verbose_name = _("Автомобіль користувача")
        verbose_name_plural = _("Автомобілі користувачів")
