from django.core.management.base import BaseCommand
from services.models import ServiceCategory, Service
from cars.models import CarBrand, CarModel
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Seed database with services and car brands'

    def handle(self, *args, **options):
        self.stdout.write('Creating service categories and services...')
        
        # Service Categories
        categories_data = [
            {'name': 'Двигун', 'icon': 'settings'},
            {'name': 'Ходова частина', 'icon': 'disc'},
            {'name': 'Гальмівна система', 'icon': 'circle'},
            {'name': 'Електрика', 'icon': 'zap'},
            {'name': 'Кузов', 'icon': 'car'},
            {'name': 'Клімат-контроль', 'icon': 'wind'},
            {'name': 'Запчастини', 'icon': 'package'},
        ]
        
        for cat_data in categories_data:
            cat, created = ServiceCategory.objects.get_or_create(name=cat_data['name'])
            if created:
                cat.icon = cat_data['icon']
                cat.save()
        
        # Services
        services_data = [
            # Двигун
            {'category': 'Двигун', 'name': 'Заміна моторної оливи', 'description': 'Повна заміна моторного мастила та масляного фільтра', 'base_price': 800, 'hours': 1},
            {'category': 'Двигун', 'name': 'Заміна оливи в КПП', 'description': 'Заміна мастила в механічній або автоматичній коробці передач', 'base_price': 1200, 'hours': 2},
            {'category': 'Двигун', 'name': 'Заміна повітряного фільтра', 'description': 'Заміна фільтра повітря двигуна', 'base_price': 300, 'hours': 0.5},
            {'category': 'Двигун', 'name': 'Заміна паливного фільтра', 'description': 'Заміна фільтра палива', 'base_price': 500, 'hours': 1},
            {'category': 'Двигун', 'name': 'Заміна ременя ГРМ', 'description': 'Заміна ременя газорозподільного механізму', 'base_price': 2500, 'hours': 4},
            {'category': 'Двигун', 'name': 'Заміна ланцюга ГРМ', 'description': 'Заміна ланцюга газорозподільного механізму', 'base_price': 4000, 'hours': 6},
            {'category': 'Двигун', 'name': 'Діагностика двигуна', 'description': 'Комп\'ютерна діагностика двигуна та системи управління', 'base_price': 500, 'hours': 1},
            {'category': 'Двигун', 'name': 'Заміна свечей запалювання', 'description': 'Заміна свічок запалювання', 'base_price': 400, 'hours': 1},
            {'category': 'Двигун', 'name': 'Промивка форсунок', 'description': 'Ультразвукова промивка форсунок', 'base_price': 1500, 'hours': 2},
            {'category': 'Двигун', 'name': 'Заміна термостату', 'description': 'Заміна термостату системи охолодження', 'base_price': 800, 'hours': 1},
            
            # Ходова частина
            {'category': 'Ходова частина', 'name': 'Заміна амортизаторів', 'description': 'Заміна передніх або задніх амортизаторів', 'base_price': 1600, 'hours': 2},
            {'category': 'Ходова частина', 'name': 'Заміна стійок стабілізатора', 'description': 'Заміна стійок поперечної стійкості', 'base_price': 600, 'hours': 1},
            {'category': 'Ходова частина', 'name': 'Заміна кульових опор', 'description': 'Заміна кульових опор передньої підвіски', 'base_price': 800, 'hours': 1},
            {'category': 'Ходова частина', 'name': 'Заміна наконечників керма', 'description': 'Заміна рульових наконечників', 'base_price': 500, 'hours': 1},
            {'category': 'Ходова частина', 'name': 'Заміна сайлент-блоків', 'description': 'Заміна гумометалевих з\'єднань підвіски', 'base_price': 1200, 'hours': 2},
            {'category': 'Ходова частина', 'name': 'Розвал-сходження', 'description': 'Регулювання кутів коліс', 'base_price': 800, 'hours': 1},
            {'category': 'Ходова частина', 'name': 'Заміна ШРУС', 'description': 'Заміна шарніра рівних кутових швидкостей', 'base_price': 1200, 'hours': 2},
            {'category': 'Ходова частина', 'name': 'Заміна підшипника маточини', 'description': 'Заміна підшипника передньої або задньої маточини', 'base_price': 1000, 'hours': 1.5},
            
            # Гальмівна система
            {'category': 'Гальмівна система', 'name': 'Заміна гальмівних колодок', 'description': 'Заміна передніх або задніх гальмівних колодок', 'base_price': 800, 'hours': 1},
            {'category': 'Гальмівна система', 'name': 'Заміна гальмівних дисків', 'description': 'Заміна передніх або задніх гальмівних дисків', 'base_price': 1400, 'hours': 1.5},
            {'category': 'Гальмівна система', 'name': 'Заміна гальмівного супорта', 'description': 'Заміна гальмівного супорта', 'base_price': 2000, 'hours': 2},
            {'category': 'Гальмівна система', 'name': 'Заміна гальмівного циліндра', 'description': 'Заміна головного або робочого циліндра', 'base_price': 1200, 'hours': 2},
            {'category': 'Гальмівна система', 'name': 'Прокачка гальм', 'description': 'Прокачка гальмівної системи', 'base_price': 400, 'hours': 1},
            {'category': 'Гальмівна система', 'name': 'Заміна тросика ручника', 'description': 'Заміна троса стояночного гальма', 'base_price': 800, 'hours': 1.5},
            
            # Електрика
            {'category': 'Електрика', 'name': 'Діагностика електрики', 'description': 'Комп\'ютерна діагностика електросистем', 'base_price': 400, 'hours': 1},
            {'category': 'Електрика', 'name': 'Заміна акумулятора', 'description': 'Заміна та обслуговування акумулятора', 'base_price': 300, 'hours': 0.5},
            {'category': 'Електрика', 'name': 'Заміна генератора', 'description': 'Зняття та встановлення генератора', 'base_price': 2000, 'hours': 3},
            {'category': 'Електрика', 'name': 'Заміна стартера', 'description': 'Зняття та встановлення стартера', 'base_price': 1800, 'hours': 3},
            {'category': 'Електрика', 'name': 'Ремонт проводки', 'description': 'Ремонт електричної проводки автомобіля', 'base_price': 1000, 'hours': 2},
            {'category': 'Електрика', 'name': 'Встановлення сигналізації', 'description': 'Монтаж автосигналізації', 'base_price': 2500, 'hours': 4},
            {'category': 'Електрика', 'name': 'Встановлення парктроніків', 'description': 'Монтаж системи паркування', 'base_price': 1500, 'hours': 2},
            {'category': 'Електрика', 'name': 'Встановлення камери заднього виду', 'description': 'Монтаж камери заднього виду', 'base_price': 2000, 'hours': 3},
            
            # Кузов
            {'category': 'Кузов', 'name': 'Полірування кузова', 'description': 'Полірування лакофарбового покриття', 'base_price': 2000, 'hours': 3},
            {'category': 'Кузов', 'name': 'Керамічне покриття', 'description': 'Нанесення керамічного захисту кузова', 'base_price': 8000, 'hours': 8},
            {'category': 'Кузов', 'name': 'Антикорозійна обробка', 'description': 'Обробка кузова антикорозійними матеріалами', 'base_price': 3000, 'hours': 4},
            {'category': 'Кузов', 'name': 'Ремінт подряпин', 'description': 'Локальний ремонт подряпин на кузові', 'base_price': 1500, 'hours': 2},
            {'category': 'Кузов', 'name': 'Заміна скла', 'description': 'Заміна лобового або бічного скла', 'base_price': 2000, 'hours': 2},
            {'category': 'Кузов', 'name': 'Фарбування елементів', 'description': 'Фарбування бампера, капота або дверей', 'base_price': 4000, 'hours': 6},
            
            # Клімат-контроль
            {'category': 'Клімат-контроль', 'name': 'Заправка кондиціонера', 'description': 'Заправка системи кондиціонування фреоном', 'base_price': 800, 'hours': 1},
            {'category': 'Клімат-контроль', 'name': 'Дезінфекція кондиціонера', 'description': 'Антибактеріальна обробка системи кондиціонування', 'base_price': 600, 'hours': 1},
            {'category': 'Клімат-контроль', 'name': 'Заміна салонного фільтра', 'description': 'Заміна фільтра салона', 'base_price': 300, 'hours': 0.5},
            {'category': 'Клімат-контроль', 'name': 'Ремонт кондиціонера', 'description': 'Діагностика та ремонт системи кондиціонування', 'base_price': 1500, 'hours': 2},
            {'category': 'Клімат-контроль', 'name': 'Заміна радіатора пічки', 'description': 'Заміна радіатора опалювача', 'base_price': 1800, 'hours': 3},
            
            # Запчастини
            {'category': 'Запчастини', 'name': 'Підбір запчастин', 'description': 'Підбір оригінальних та аналогових запчастин', 'base_price': 0, 'hours': 0},
            {'category': 'Запчастини', 'name': 'Встановлення запчастин', 'description': 'Монтаж придбаних запчастин', 'base_price': 500, 'hours': 1},
        ]
        
        for svc_data in services_data:
            category = ServiceCategory.objects.get(name=svc_data['category'])
            service, created = Service.objects.get_or_create(
                name=svc_data['name'],
                category=category,
                defaults={
                    'description': svc_data['description'],
                    'base_price': svc_data['base_price'],
                    'estimated_time': timedelta(hours=svc_data['hours'])
                }
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(services_data)} services'))
        
        # Car Brands and Models
        self.stdout.write('Creating car brands and models...')
        
        brands_models = [
            {'brand': 'Toyota', 'models': ['Corolla', 'Camry', 'RAV4', 'Land Cruiser', 'Highlander', 'Prius', 'C-HR', 'Yaris', 'Avensis', 'Verso']},
            {'brand': 'BMW', 'models': ['3 Series', '5 Series', '7 Series', 'X3', 'X5', 'X7', 'X1', 'X6', 'M3', 'M5']},
            {'brand': 'Mercedes-Benz', 'models': ['C-Class', 'E-Class', 'S-Class', 'GLC', 'GLE', 'GLS', 'A-Class', 'B-Class', 'CLA', 'GLA']},
            {'brand': 'Audi', 'models': ['A3', 'A4', 'A6', 'A8', 'Q3', 'Q5', 'Q7', 'Q8', 'TT', 'R8']},
            {'brand': 'Volkswagen', 'models': ['Golf', 'Passat', 'Tiguan', 'Polo', 'Touareg', 'Arteon', 'Jetta', 'T-Roc', 'Caddy', 'Amarok']},
            {'brand': 'Ford', 'models': ['Focus', 'Mondeo', 'Kuga', 'EcoSport', 'Explorer', 'Mustang', 'Fiesta', 'Ranger', 'Edge', 'Transit']},
            {'brand': 'Honda', 'models': ['Civic', 'Accord', 'CR-V', 'HR-V', 'Pilot', 'Odyssey', 'Jazz', 'Insight', 'Ridgeline', 'FR-V']},
            {'brand': 'Hyundai', 'models': ['Elantra', 'Sonata', 'Tucson', 'Santa Fe', 'Creta', 'Kona', 'Palisade', 'Starex', 'Accent', 'Ioniq']},
            {'brand': 'Kia', 'models': ['Optima', 'Forte', 'Sportage', 'Sorento', 'Telluride', 'Stonic', 'Ceed', 'Rio', 'Carnival', 'Seltos']},
            {'brand': 'Nissan', 'models': ['Altima', 'Maxima', 'Rogue', 'Pathfinder', 'Murano', 'Qashqai', 'Juke', 'Leaf', 'X-Trail', 'Armada']},
            {'brand': 'Mazda', 'models': ['Mazda3', 'Mazda6', 'CX-5', 'CX-9', 'CX-30', 'MX-5', 'CX-3', 'CX-50', 'MX-30', 'RX-8']},
            {'brand': 'Volvo', 'models': ['S60', 'S90', 'V60', 'V90', 'XC40', 'XC60', 'XC90', 'XC70', 'S80', 'V40']},
            {'brand': 'Porsche', 'models': ['911', 'Cayenne', 'Macan', 'Panamera', 'Taycan', 'Cayman', 'Boxster']},
            {'brand': 'Lexus', 'models': ['ES', 'IS', 'GS', 'LS', 'RX', 'NX', 'LX', 'UX', 'GX', 'LC']},
            {'brand': 'Subaru', 'models': ['Outback', 'Forester', 'Impreza', 'Legacy', 'XV', 'BRZ', 'WRX', 'Crosstrek', 'Ascent', 'Solterra']},
            {'brand': 'Mitsubishi', 'models': ['Outlander', 'Pajero', 'Lancer', 'Eclipse Cross', 'ASX', 'Montero', 'Space Star', 'Attrage', 'Xpander', 'L200']},
            {'brand': 'Peugeot', 'models': ['208', '308', '508', '2008', '3008', '5008', 'Partner', 'Rifter', 'Traveller', 'Boxer']},
            {'brand': 'Renault', 'models': ['Clio', 'Megane', 'Talisman', 'Kadjar', 'Koleos', 'Arkana', 'Duster', 'Sandero', 'Logan', 'Trafic']},
            {'brand': 'Citroen', 'models': ['C3', 'C4', 'C5', 'C5 Aircross', 'C3 Aircross', 'Berlingo', 'Jumpy', 'SpaceTourer', 'DS3', 'DS7']},
            {'brand': 'Chery', 'models': ['Tiggo 4', 'Tiggo 7', 'Tiggo 8', 'Exeed TXL', 'Omoda C5', 'Arrizo 8', 'Tiggo 2', 'Bonus', 'Very', 'M11']},
        ]
        
        total_models = 0
        for brand_data in brands_models:
            brand, created = CarBrand.objects.get_or_create(name=brand_data['brand'])
            for model_name in brand_data['models']:
                model, model_created = CarModel.objects.get_or_create(
                    brand=brand,
                    name=model_name,
                    defaults={'year_start': 2015}
                )
                if model_created:
                    total_models += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {total_models} car models'))
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
