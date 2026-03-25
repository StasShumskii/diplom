import json
from decimal import Decimal

from cars.models import CarBrand, CarModel, UserCar
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from services.models import Service, ServiceCategory

from .models import CalculationLog


class CalculatorView(TemplateView):
    template_name = "calculator/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["brands"] = CarBrand.objects.all()
        context["services"] = Service.objects.all()
        context["categories"] = ServiceCategory.objects.all()

        if self.request.user.is_authenticated:
            context["cars"] = UserCar.objects.filter(user=self.request.user)

        return context


def api_calculate_estimate(request):
    """
    HTMX Endpoint for live calculation
    """
    brand_id = request.GET.get("brand")
    model_id = request.GET.get("model")
    service_ids = request.GET.getlist("services")
    year = int(request.GET.get("year", 2024))
    mileage = int(request.GET.get("mileage", 0))

    services = Service.objects.filter(id__in=service_ids)
    base_total = sum(s.base_price for s in services)

    # 2026 Logic: Age & Mileage Multipliers
    age = 2026 - year
    multiplier = Decimal("1.0")

    if age > 10:
        multiplier += Decimal("0.3")
    elif age > 5:
        multiplier += Decimal("0.15")

    if mileage > 200000:
        multiplier += Decimal("0.25")
    elif mileage > 100000:
        multiplier += Decimal("0.1")

    final_total = base_total * multiplier

    # AI Recommendations
    recommendations = []
    if mileage > 150000:
        recommendations.append("Рекомендовано перевірити стан ГРМ")
    if age > 7:
        recommendations.append("Можлива корозія кріплень підвіски")

    context = {"total": final_total, "recommendations": recommendations, "multiplier": multiplier}

    return render(request, "calculator/partials/result.html", context)


def api_get_models(request):
    """
    HTMX Endpoint for dynamic model dropdown
    """
    brand_id = request.GET.get("brand")
    models = CarModel.objects.filter(brand_id=brand_id)
    return render(request, "calculator/partials/model_options.html", {"models": models})
