from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from .models import CarBrand, CarModel, UserCar


@login_required
def car_list(request):
    cars = UserCar.objects.filter(user=request.user)
    return render(request, "cars/list.html", {"cars": cars})


def api_get_models(request):
    brand_id = request.GET.get("brand")
    if brand_id:
        models = CarModel.objects.filter(brand_id=brand_id)
        return render(request, "calculator/partials/model_options.html", {"models": models})
    return JsonResponse({"models": []})


@login_required
def add_car_ajax(request):
    if request.method == "POST":
        brand_id = request.POST.get("brand")
        model_id = request.POST.get("model")
        year = request.POST.get("year")
        license_plate = request.POST.get("license_plate")
        vin = request.POST.get("vin")
        mileage = request.POST.get("mileage", 0)
        engine_type = request.POST.get("engine_type")
        engine_volume = request.POST.get("engine_volume")
        fuel_type = request.POST.get("fuel_type")
        technical_condition = request.POST.get("technical_condition", "GOOD")

        try:
            car_model = CarModel.objects.get(id=model_id)
            car = UserCar.objects.create(
                user=request.user,
                model=car_model,
                year=int(year),
                license_plate=license_plate,
                vin=vin if vin else None,
                mileage=int(mileage) if mileage else 0,
                engine_type=engine_type if engine_type else None,
                engine_volume=float(engine_volume) if engine_volume else None,
                fuel_type=fuel_type if fuel_type else None,
                technical_condition=technical_condition if technical_condition else "GOOD",
            )
            return JsonResponse({"status": "success", "message": "Авто додано успішно!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request"})
