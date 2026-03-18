import os
import django
import random
from datetime import timedelta
from django.utils import timezone
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auto_service.settings')
django.setup()

from accounts.models import User
from services.models import Service, ServiceCategory, Part
from cars.models import CarBrand, CarModel, UserCar
from bookings.models import Booking, OrderItem

def seed_data():
    print("--- Початкове наповнення бази даних AutoPro 2026 ---")

    # 1. Створення категорій
    categories_data = [
        {'name': 'Технічне обслуговування', 'icon': 'wrench'},
        {'name': 'Діагностика та електроніка', 'icon': 'cpu'},
        {'name': 'Трансмісія та двигун', 'icon': 'settings'},
        {'name': 'Кузов та детейлінг', 'icon': 'sparkles'},
        {'name': 'Ходова частина', 'icon': 'shield-check'},
    ]
    categories = []
    for cat in categories_data:
        c, _ = ServiceCategory.objects.get_or_create(name=cat['name'], icon=cat['icon'])
        categories.append(c)

    # 2. Створення послуг
    services_list = [
        ('Заміна мастила та фільтрів', 1500, 1, 0),
        ('Комп’ютерна діагностика', 800, 0, 1),
        ('Чистка форсунок', 1200, 2, 2),
        ('Регулювання розвалу-сходження', 600, 4, 0),
        ('Нанесення кераміки (Premium)', 12000, 3, 40),
        ('Заміна гальмівних колодок', 900, 4, 1),
        ('Ремонт АКПП (Складний)', 25000, 2, 120),
        ('Чіп-тюнінг AI Stage 1', 8000, 1, 4),
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

    # 3. Марки та моделі (Масивний набір)
    brands_data = {
        'BMW': ['M3', 'M5', 'X5', 'X7', 'iX'],
        'Audi': ['A6', 'A8', 'Q7', 'Q8', 'e-tron'],
        'Mercedes-Benz': ['S-Class', 'G-Class', 'GLE', 'EQS'],
        'Porsche': ['911', 'Cayenne', 'Taycan', 'Panamera'],
        'Tesla': ['Model S', 'Model X', 'Model 3', 'Model Y'],
        'Toyota': ['Camry', 'Land Cruiser', 'RAV4'],
        'Lexus': ['RX', 'LX', 'ES', 'LS'],
    }
    all_models = []
    for brand_name, models in brands_data.items():
        brand, _ = CarBrand.objects.get_or_create(name=brand_name)
        for m_name in models:
            m, _ = CarModel.objects.get_or_create(brand=brand, name=m_name, defaults={'year_start': 2015})
            all_models.append(m)

    # 4. Користувачі
    # Manager
    mngr, _ = User.objects.get_or_create(email='manager@gmail.com', defaults={'username': 'manager', 'role': 'MANAGER', 'is_staff': True})
    mngr.set_password('admin123')
    mngr.save()

    # Client
    client, _ = User.objects.get_or_create(email='client@gmail.com', defaults={'username': 'client', 'role': 'CLIENT'})
    client.set_password('pass123')
    client.save()
    clients = [client]

    # Mechanic
    mech, _ = User.objects.get_or_create(username='mechanic', defaults={'role': 'MECHANIC', 'is_staff': True})
    mech.set_password('admin123')
    mech.save()
    mechanics = [mech]

    # 5. Автомобілі користувачів
    for client in clients:
        for _ in range(random.randint(1, 2)):
            UserCar.objects.create(
                user=client,
                model=random.choice(all_models),
                license_plate=f"KA {random.randint(1000, 9999)} AA",
                year=random.randint(2018, 2025),
                mileage=random.randint(10000, 150000)
            )

    # 6. Записи на сервіс (Професійний набір)
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

    print("--- Наповнення завершено! База готова до презентації. ---")

if __name__ == '__main__':
    seed_data()
