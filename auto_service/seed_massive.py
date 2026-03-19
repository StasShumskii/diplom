import os
import django
import random
from datetime import timedelta
from django.utils import timezone
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auto_service.settings')
django.setup()

from accounts.models import User
from services.models import Service, ServiceCategory, Part
from cars.models import CarBrand, CarModel, UserCar
from bookings.models import Booking, OrderItem

def seed_data():
    print("--- Початкове наповнення бази даних AutoPro 2026 ---")

    categories_data = [
        {'name': 'Технічне обслуговування', 'icon': 'wrench'},
        {'name': 'Діагностика та електроніка', 'icon': 'cpu'},
        {'name': 'Трансмісія та двигун', 'icon': 'settings'},
        {'name': 'Кузов та детейлінг', 'icon': 'sparkles'},
        {'name': 'Ходова частина', 'icon': 'shield-check'},
        {'name': 'Гальмівна система', 'icon': 'disc'},
        {'name': 'Кондиціонування', 'icon': 'thermometer'},
    ]
    categories = []
    for cat in categories_data:
        c, _ = ServiceCategory.objects.get_or_create(name=cat['name'], icon=cat['icon'])
        categories.append(c)

    services_list = [
        ('Заміна мастила та фільтрів', 1500, 0, 1),
        ('Заміна повітряного фільтра', 400, 0, 0.5),
        ('Заміна салонного фільтра', 350, 0, 0.5),
        ('Заміна гальмівної рідини', 600, 0, 1),
        ('Заміна антифризу', 800, 0, 1),
        ('Заміна свічок запалювання', 600, 0, 0.5),
        ('ТО-1 (масло + фільтри)', 2000, 0, 1),
        ('ТО-2 (повний комплекс)', 4500, 0, 3),
        ('Комп\'ютерна діагностика', 800, 1, 1),
        ('Діагностика двигуна (повна)', 1500, 1, 2),
        ('Діагностика підвіски', 600, 1, 1),
        ('Діагностика гальмівної системи', 500, 1, 1),
        ('Кодування ключів', 1200, 1, 1),
        ('Усунення помилок SRS', 800, 1, 1),
        ('Налаштування ECU', 2000, 1, 2),
        ('Чистка форсунок', 1200, 2, 2),
        ('Ремонт АКПП', 25000, 2, 120),
        ('Ремонт МКПП', 8000, 2, 8),
        ('Заміна зчеплення', 6000, 2, 6),
        ('Ремонт двигуна (капітальний)', 35000, 2, 48),
        ('Ремонт ГБЦ', 8000, 2, 12),
        ('Заміна ременя ГРМ', 2500, 2, 3),
        ('Чіп-тюнінг AI Stage 1', 8000, 2, 4),
        ('Чіп-тюнінг AI Stage 2', 12000, 2, 4),
        ('Нанесення кераміки (Premium)', 12000, 3, 40),
        ('Полірування кузова', 3500, 3, 6),
        ('Хімчистка салону', 2500, 3, 8),
        ('Керамічне покриття', 8000, 3, 24),
        ('Антикорозійна обробка', 4000, 3, 6),
        ('Ремонт подряпин', 1500, 3, 2),
        ('Заміна скла', 3000, 3, 3),
        ('Регулювання розвалу-сходження', 600, 4, 1),
        ('Заміна гальмівних колодок', 900, 4, 1),
        ('Заміна гальмівних дисків', 1800, 4, 2),
        ('Заміна амортизаторів', 2400, 4, 2),
        ('Заміна стійок стабілізатора', 600, 4, 0.5),
        ('Заміна підшипників ступиці', 1200, 4, 1.5),
        ('Ремонт рульової рейки', 5000, 4, 6),
        ('Заміна ШРУСА', 2000, 4, 2),
        ('Заправка кондиціонера', 1200, 6, 1),
        ('Чистка кондиціонера', 1500, 6, 2),
        ('Ремонт компресора кондиціонера', 6000, 6, 8),
        ('Заміна радіатора пічки', 3500, 6, 4),
    ]
    all_services = []
    for name, price, cat_idx, hours in services_list:
        s, _ = Service.objects.get_or_create(
            name=name,
            defaults={
                'category': categories[cat_idx],
                'base_price': price,
                'estimated_time': timedelta(hours=hours if hours > 0 else 1)
            }
        )
        all_services.append(s)

    brands_data = {
        'BMW': ['M3', 'M5', 'X5', 'X7', 'iX', 'X3', 'X1', '5 Series', '3 Series', '7 Series'],
        'Audi': ['A6', 'A8', 'Q7', 'Q8', 'e-tron', 'Q5', 'Q3', 'A4', 'A3', 'TT'],
        'Mercedes-Benz': ['S-Class', 'G-Class', 'GLE', 'EQS', 'C-Class', 'E-Class', 'GLC', 'GLA'],
        'Porsche': ['911', 'Cayenne', 'Taycan', 'Panamera', 'Macan'],
        'Tesla': ['Model S', 'Model X', 'Model 3', 'Model Y', 'Cybertruck'],
        'Toyota': ['Camry', 'Land Cruiser', 'RAV4', 'Corolla', 'Highlander', 'Prado', 'Fortuner'],
        'Lexus': ['RX', 'LX', 'ES', 'LS', 'NX', 'UX'],
        'Volkswagen': ['Golf', 'Passat', 'Tiguan', 'Touareg', 'Arteon', 'Polo'],
        'Ford': ['Mustang', 'Explorer', 'Kuga', 'Focus', 'Ranger'],
        'Honda': ['Civic', 'Accord', 'CR-V', 'Pilot', 'HR-V'],
        'Hyundai': ['Tucson', 'Santa Fe', 'Sonata', 'Elantra', 'Creta', 'Palisade'],
        'Kia': ['Sportage', 'Sorento', 'Optima', 'Stinger', 'Telluride', 'Seltos'],
        'Nissan': ['Altima', 'Murano', 'Pathfinder', 'Qashqai', 'X-Trail'],
        'Mazda': ['CX-5', 'CX-9', 'Mazda6', 'MX-5', 'CX-30'],
        'Subaru': ['Outback', 'Forester', 'XV', 'Legacy', 'Impreza'],
        'Jeep': ['Grand Cherokee', 'Wrangler', 'Cherokee', 'Compass'],
        'Land Rover': ['Range Rover', 'Discovery', 'Defender', 'Evoque'],
        'Volvo': ['XC90', 'XC60', 'XC40', 'S90', 'V90'],
        'Renault': ['Duster', 'Koleos', 'Arkana', 'Megane', 'Kadjar'],
        'Peugeot': ['3008', '5008', '508', 'RCZ'],
        'Citroen': ['C5 Aircross', 'C3', 'SpaceTourer'],
    }
    all_models = []
    for brand_name, models in brands_data.items():
        brand, _ = CarBrand.objects.get_or_create(name=brand_name)
        for m_name in models:
            m, _ = CarModel.objects.get_or_create(brand=brand, name=m_name, defaults={'year_start': 2015})
            all_models.append(m)

    mngr, _ = User.objects.get_or_create(email='manager@gmail.com', defaults={'username': 'manager', 'role': 'MANAGER', 'is_staff': True})
    mngr.set_password('admin123')
    mngr.save()

    client, _ = User.objects.get_or_create(email='client@gmail.com', defaults={'username': 'client', 'role': 'CLIENT'})
    client.set_password('pass123')
    client.save()
    clients = [client]

    mech, _ = User.objects.get_or_create(username='mechanic', defaults={'role': 'MECHANIC', 'is_staff': True})
    mech.set_password('admin123')
    mech.save()
    mechanics = [mech]

    for client in clients:
        for _ in range(random.randint(1, 2)):
            UserCar.objects.create(
                user=client,
                model=random.choice(all_models),
                license_plate=f"KA {random.randint(1000, 9999)} AA",
                year=random.randint(2018, 2025),
                mileage=random.randint(10000, 150000)
            )

    statuses = [s[0] for s in Booking.Status.choices]
    all_user_cars = UserCar.objects.all()
    
    for _ in range(30):
        car = random.choice(all_user_cars)
        selected_services = random.sample(all_services, random.randint(1, 3))
        total = sum(s.base_price for s in selected_services)
        
        booking = Booking.objects.create(
            client=car.user,
            car=car,
            mechanic=random.choice(mechanics) if random.random() > 0.3 else None,
            scheduled_at=timezone.now() + timedelta(days=random.randint(-15, 15)),
            status=random.choice(statuses),
            total_cost=total,
            notes="Автоматично згенерований запис для презентації системи."
        )
        
        for s in selected_services:
            OrderItem.objects.create(booking=booking, service=s, price_at_booking=s.base_price)

    print("--- Наповнення завершено! ---")

if __name__ == '__main__':
    seed_data()
