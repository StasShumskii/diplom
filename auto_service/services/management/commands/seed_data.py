from django.core.management.base import BaseCommand
from services.models import ServiceCategory, Service
from cars.models import CarBrand, CarModel
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Seed database with services and car brands'

    def handle(self, *args, **options):
        self.stdout.write('Creating service categories and services...')
        
        categories_data = [
            {'name': 'Двигун', 'icon': 'settings'},
            {'name': 'Ходова частина', 'icon': 'disc'},
            {'name': 'Гальмівна система', 'icon': 'circle'},
            {'name': 'Електрика', 'icon': 'zap'},
            {'name': 'Кузов', 'icon': 'car'},
            {'name': 'Клімат-контроль', 'icon': 'wind'},
            {'name': 'Запчастини', 'icon': 'package'},
            {'name': 'Трансмісія', 'icon': 'git-merge'},
            {'name': 'Рульове управління', 'icon': 'move'},
            {'name': 'Скло та світло', 'icon': 'sun'},
            {'name': 'ТО та діагностика', 'icon': 'activity'},
            {'name': 'Додаткові послуги', 'icon': 'plus-circle'},
        ]
        
        for cat_data in categories_data:
            cat, created = ServiceCategory.objects.get_or_create(name=cat_data['name'])
            if created:
                cat.icon = cat_data['icon']
                cat.save()
        
        services_data = [
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
            {'category': 'Двигун', 'name': 'Заміна водяної помпи', 'description': 'Заміна помпи системи охолодження', 'base_price': 1200, 'hours': 2},
            {'category': 'Двигун', 'name': 'Заміна радіатора', 'description': 'Заміна радіатора охолодження двигуна', 'base_price': 2000, 'hours': 3},
            {'category': 'Двигун', 'name': 'Ремонт головки блоку', 'description': 'Ремонт або заміна ГБЦ', 'base_price': 5000, 'hours': 8},
            {'category': 'Двигун', 'name': 'Капітальний ремонт двигуна', 'description': 'Повний капітальний ремонт двигуна', 'base_price': 25000, 'hours': 40},
            {'category': 'Двигун', 'name': 'Заміна прокладки ГБЦ', 'description': 'Заміна прокладки головки блоку циліндрів', 'base_price': 3000, 'hours': 5},
            {'category': 'Двигун', 'name': 'Заміна маслоснимателей', 'description': 'Заміна маслоснімательних колпачків', 'base_price': 1800, 'hours': 3},
            {'category': 'Двигун', 'name': 'Регулювання клапанів', 'description': 'Регулювання теплових зазорів клапанів', 'base_price': 1200, 'hours': 2},
            {'category': 'Двигун', 'name': 'Заміна піддону картера', 'description': 'Заміна піддону картера двигуна', 'base_price': 1000, 'hours': 1.5},
            {'category': 'Двигун', 'name': 'Діагностика турбіни', 'description': 'Діагностика та перевірка турбокомпресора', 'base_price': 800, 'hours': 1},
            {'category': 'Двигун', 'name': 'Заміна турбіни', 'description': 'Зняття та встановлення турбокомпресора', 'base_price': 6000, 'hours': 8},
            
            {'category': 'Ходова частина', 'name': 'Заміна амортизаторів', 'description': 'Заміна передніх або задніх амортизаторів', 'base_price': 1600, 'hours': 2},
            {'category': 'Ходова частина', 'name': 'Заміна стійок стабілізатора', 'description': 'Заміна стійок поперечної стійкості', 'base_price': 600, 'hours': 1},
            {'category': 'Ходова частина', 'name': 'Заміна кульових опор', 'description': 'Заміна кульових опор передньої підвіски', 'base_price': 800, 'hours': 1},
            {'category': 'Ходова частина', 'name': 'Заміна наконечників керма', 'description': 'Заміна рульових наконечників', 'base_price': 500, 'hours': 1},
            {'category': 'Ходова частина', 'name': 'Заміна сайлент-блоків', 'description': 'Заміна гумометалевих з\'єднань підвіски', 'base_price': 1200, 'hours': 2},
            {'category': 'Ходова частина', 'name': 'Розвал-сходження', 'description': 'Регулювання кутів коліс', 'base_price': 800, 'hours': 1},
            {'category': 'Ходова частина', 'name': 'Заміна ШРУС', 'description': 'Заміна шарніра рівних кутових швидкостей', 'base_price': 1200, 'hours': 2},
            {'category': 'Ходова частина', 'name': 'Заміна підшипника маточини', 'description': 'Заміна підшипника передньої або задньої маточини', 'base_price': 1000, 'hours': 1.5},
            {'category': 'Ходова частина', 'name': 'Заміна важеля підвіски', 'description': 'Заміна верхнього або нижнього важеля', 'base_price': 900, 'hours': 1.5},
            {'category': 'Ходова частина', 'name': 'Заміна пружин підвіски', 'description': 'Заміна пружин передньої або задньої підвіски', 'base_price': 1400, 'hours': 2},
            {'category': 'Ходова частина', 'name': 'Заміна опори двигуна', 'description': 'Заміна підвісів двигуна', 'base_price': 1500, 'hours': 2},
            {'category': 'Ходова частина', 'name': 'Заміна подушки КПП', 'description': 'Заміна підвіски коробки передач', 'base_price': 1000, 'hours': 1.5},
            {'category': 'Ходова частина', 'name': 'Регулювання підвіски', 'description': 'Регулювання параметрів підвіски', 'base_price': 600, 'hours': 1},
            {'category': 'Ходова частина', 'name': 'Заміна втулок стабілізатора', 'description': 'Заміна втулок стійок стабілізатора', 'base_price': 400, 'hours': 0.5},
            {'category': 'Ходова частина', 'name': 'Заміна балки', 'description': 'Зняття та встановлення балки підвіски', 'base_price': 2000, 'hours': 3},
            
            {'category': 'Гальмівна система', 'name': 'Заміна гальмівних колодок', 'description': 'Заміна передніх або задніх гальмівних колодок', 'base_price': 800, 'hours': 1},
            {'category': 'Гальмівна система', 'name': 'Заміна гальмівних дисків', 'description': 'Заміна передніх або задніх гальмівних дисків', 'base_price': 1400, 'hours': 1.5},
            {'category': 'Гальмівна система', 'name': 'Заміна гальмівного супорта', 'description': 'Заміна гальмівного супорта', 'base_price': 2000, 'hours': 2},
            {'category': 'Гальмівна система', 'name': 'Заміна гальмівного циліндра', 'description': 'Заміна головного або робочого циліндра', 'base_price': 1200, 'hours': 2},
            {'category': 'Гальмівна система', 'name': 'Прокачка гальм', 'description': 'Прокачка гальмівної системи', 'base_price': 400, 'hours': 1},
            {'category': 'Гальмівна система', 'name': 'Заміна тросика ручника', 'description': 'Заміна троса стояночного гальма', 'base_price': 800, 'hours': 1.5},
            {'category': 'Гальмівна система', 'name': 'Заміна вакуумного підсилювача', 'description': 'Заміна вакуумного підсилювача гальм', 'base_price': 1800, 'hours': 3},
            {'category': 'Гальмівна система', 'name': 'Ремонт ABS', 'description': 'Діагностика та ремонт системи ABS', 'base_price': 1500, 'hours': 2},
            {'category': 'Гальмівна система', 'name': 'Заміна датчика ABS', 'description': 'Заміна датчика ABS', 'base_price': 600, 'hours': 1},
            {'category': 'Гальмівна система', 'name': 'Заміна гальмівних шлангів', 'description': 'Заміна гальмівних шлангів', 'base_price': 500, 'hours': 1},
            {'category': 'Гальмівна система', 'name': 'Проточка дисків', 'description': 'Проточка гальмівних дисків', 'base_price': 800, 'hours': 1.5},
            {'category': 'Гальмівна система', 'name': 'Регулювання ручника', 'description': 'Регулювання стояночного гальма', 'base_price': 300, 'hours': 0.5},
            
            {'category': 'Електрика', 'name': 'Діагностика електрики', 'description': 'Комп\'ютерна діагностика електросистем', 'base_price': 400, 'hours': 1},
            {'category': 'Електрика', 'name': 'Заміна акумулятора', 'description': 'Заміна та обслуговування акумулятора', 'base_price': 300, 'hours': 0.5},
            {'category': 'Електрика', 'name': 'Заміна генератора', 'description': 'Зняття та встановлення генератора', 'base_price': 2000, 'hours': 3},
            {'category': 'Електрика', 'name': 'Заміна стартера', 'description': 'Зняття та встановлення стартера', 'base_price': 1800, 'hours': 3},
            {'category': 'Електрика', 'name': 'Ремонт проводки', 'description': 'Ремонт електричної проводки автомобіля', 'base_price': 1000, 'hours': 2},
            {'category': 'Електрика', 'name': 'Встановлення сигналізації', 'description': 'Монтаж автосигналізації', 'base_price': 2500, 'hours': 4},
            {'category': 'Електрика', 'name': 'Встановлення парктроніків', 'description': 'Монтаж системи паркування', 'base_price': 1500, 'hours': 2},
            {'category': 'Електрика', 'name': 'Встановлення камери заднього виду', 'description': 'Монтаж камери заднього виду', 'base_price': 2000, 'hours': 3},
            {'category': 'Електрика', 'name': 'Ремонт блоку запалювання', 'description': 'Ремонт або заміна котушки запалювання', 'base_price': 800, 'hours': 1},
            {'category': 'Електрика', 'name': 'Заміна свічок розгорання', 'description': 'Заміна свічок розгорання (дизель)', 'base_price': 600, 'hours': 1},
            {'category': 'Електрика', 'name': 'Ремонт підсилювача звуку', 'description': 'Ремонт автомобільного підсилювача', 'base_price': 1200, 'hours': 2},
            {'category': 'Електрика', 'name': 'Встановлення магтоли', 'description': 'Монтаж автомагнітоли', 'base_price': 500, 'hours': 1},
            {'category': 'Електрика', 'name': 'Встановлення сабвуфера', 'description': 'Монтаж сабвуфера та акустики', 'base_price': 1500, 'hours': 3},
            {'category': 'Електрика', 'name': 'Ремонт електродвигунів', 'description': 'Ремонт склопідйомників, моторчиків', 'base_price': 800, 'hours': 1.5},
            {'category': 'Електрика', 'name': 'Діагностика ECU', 'description': 'Діагностика блоку управління двигуном', 'base_price': 600, 'hours': 1},
            {'category': 'Електрика', 'name': 'Прошивка ECU', 'description': 'Перепрошивка блоку управління двигуном', 'base_price': 3000, 'hours': 4},
            
            {'category': 'Кузов', 'name': 'Полірування кузова', 'description': 'Полірування лакофарбового покриття', 'base_price': 2000, 'hours': 3},
            {'category': 'Кузов', 'name': 'Керамічне покриття', 'description': 'Нанесення керамічного захисту кузова', 'base_price': 8000, 'hours': 8},
            {'category': 'Кузов', 'name': 'Антикорозійна обробка', 'description': 'Обробка кузова антикорозійними матеріалами', 'base_price': 3000, 'hours': 4},
            {'category': 'Кузов', 'name': 'Ремінт подряпин', 'description': 'Локальний ремонт подряпин на кузові', 'base_price': 1500, 'hours': 2},
            {'category': 'Кузов', 'name': 'Заміна скла', 'description': 'Заміна лобового або бічного скла', 'base_price': 2000, 'hours': 2},
            {'category': 'Кузов', 'name': 'Фарбування елементів', 'description': 'Фарбування бампера, капота або дверей', 'base_price': 4000, 'hours': 6},
            {'category': 'Кузов', 'name': 'Рихтування кузова', 'description': 'Рихтування пошкоджених елементів кузова', 'base_price': 2500, 'hours': 4},
            {'category': 'Кузов', 'name': 'Зварювання кузова', 'description': 'Зварювальні роботи по кузову', 'base_price': 2000, 'hours': 3},
            {'category': 'Кузов', 'name': 'Заміна бампера', 'description': 'Зняття та встановлення бампера', 'base_price': 1200, 'hours': 2},
            {'category': 'Кузов', 'name': 'Заміна капота', 'description': 'Зняття та встановлення капота', 'base_price': 1000, 'hours': 1.5},
            {'category': 'Кузов', 'name': 'Заміна крила', 'description': 'Зняття та встановлення крила', 'base_price': 1500, 'hours': 2},
            {'category': 'Кузов', 'name': 'Полірування фар', 'description': 'Відновлення прозорості фар', 'base_price': 800, 'hours': 1.5},
            {'category': 'Кузов', 'name': 'Бронеплёнка', 'description': 'Нанесення антигравійної плівки', 'base_price': 5000, 'hours': 6},
            {'category': 'Кузов', 'name': 'Хімчистка салону', 'description': 'Повна хімчистка салону автомобіля', 'base_price': 2500, 'hours': 4},
            {'category': 'Кузов', 'name': 'Мийка двигуна', 'description': 'Мийка та консервація двигуна', 'base_price': 1200, 'hours': 2},
            {'category': 'Кузов', 'name': 'Керамічне скло', 'description': 'Нанесення керамічного покриття на скло', 'base_price': 1500, 'hours': 2},
            
            {'category': 'Клімат-контроль', 'name': 'Заправка кондиціонера', 'description': 'Заправка системи кондиціонування фреоном', 'base_price': 800, 'hours': 1},
            {'category': 'Клімат-контроль', 'name': 'Дезінфекція кондиціонера', 'description': 'Антибактеріальна обробка системи кондиціонування', 'base_price': 600, 'hours': 1},
            {'category': 'Клімат-контроль', 'name': 'Заміна салонного фільтра', 'description': 'Заміна фільтра салона', 'base_price': 300, 'hours': 0.5},
            {'category': 'Клімат-контроль', 'name': 'Ремонт кондиціонера', 'description': 'Діагностика та ремонт системи кондиціонування', 'base_price': 1500, 'hours': 2},
            {'category': 'Клімат-контроль', 'name': 'Заміна радіатора пічки', 'description': 'Заміна радіатора опалювача', 'base_price': 1800, 'hours': 3},
            {'category': 'Клімат-контроль', 'name': 'Заміна компресора кондиціонера', 'description': 'Зняття та встановлення компресора', 'base_price': 4000, 'hours': 6},
            {'category': 'Клімат-контроль', 'name': 'Пошук витоку фреону', 'description': 'Діагностика та пошук витоку холодоагенту', 'base_price': 600, 'hours': 1},
            {'category': 'Клімат-контроль', 'name': 'Заміна трубок кондиціонера', 'description': 'Заміна магістралей кондиціонування', 'base_price': 2000, 'hours': 3},
            {'category': 'Клімат-контроль', 'name': 'Ремонт пічки', 'description': 'Ремонт системи опалення', 'base_price': 1200, 'hours': 2},
            {'category': 'Клімат-контроль', 'name': 'Заміна вентилятора', 'description': 'Заміна вентилятора охолодження', 'base_price': 1000, 'hours': 1.5},
            
            {'category': 'Трансмісія', 'name': 'Заміна зчеплення', 'description': 'Заміна диска та корзини зчеплення', 'base_price': 3500, 'hours': 5},
            {'category': 'Трансмісія', 'name': 'Ремонт КПП механіка', 'description': 'Ремонт механічної коробки передач', 'base_price': 5000, 'hours': 8},
            {'category': 'Трансмісія', 'name': 'Ремонт КПП автомат', 'description': 'Ремонт автоматичної коробки передач', 'base_price': 8000, 'hours': 12},
            {'category': 'Трансмісія', 'name': 'Заміна мастила в раздаточній коробці', 'description': 'Заміна мастила в роздавальній коробці', 'base_price': 800, 'hours': 1},
            {'category': 'Трансмісія', 'name': 'Заміна приводних валів', 'description': 'Заміна правого або лівого приводного вала', 'base_price': 1800, 'hours': 2.5},
            {'category': 'Трансмісія', 'name': 'Ремонт диференціала', 'description': 'Ремонт або заміна диференціала', 'base_price': 4000, 'hours': 6},
            {'category': 'Трансмісія', 'name': 'Заміна вилки зчеплення', 'description': 'Заміна вилки виключення зчеплення', 'base_price': 1500, 'hours': 2},
            {'category': 'Трансмісія', 'name': 'Регулювання КПП', 'description': 'Регулювання механічної коробки передач', 'base_price': 600, 'hours': 1},
            {'category': 'Трансмісія', 'name': 'Заміна підшипника вижимного', 'description': 'Заміна підшипника виключення зчеплення', 'base_price': 1200, 'hours': 2},
            
            {'category': 'Рульове управління', 'name': 'Заміна рульової рейки', 'description': 'Зняття та встановлення рульової рейки', 'base_price': 4000, 'hours': 6},
            {'category': 'Рульове управління', 'name': 'Ремонт рульової рейки', 'description': 'Ремонт рульової рейки', 'base_price': 2500, 'hours': 4},
            {'category': 'Рульове управління', 'name': 'Заміна гідравлічного насоса', 'description': 'Заміна ГУР', 'base_price': 3000, 'hours': 4},
            {'category': 'Рульове управління', 'name': 'Заміна рульового вала', 'description': 'Заміна рульового вала', 'base_price': 2000, 'hours': 3},
            {'category': 'Рульове управління', 'name': 'Заміна наконечників', 'description': 'Заміна рульових наконечників', 'base_price': 700, 'hours': 1},
            {'category': 'Рульове управління', 'name': 'Заміна тяг', 'description': 'Заміна рульових тяг', 'base_price': 900, 'hours': 1.5},
            {'category': 'Рульове управління', 'name': 'Прокачка ГУР', 'description': 'Прокачка гідропідсилювача керма', 'base_price': 500, 'hours': 1},
            {'category': 'Рульове управління', 'name': 'Заміна рідини ГУР', 'description': 'Заміна гідравлічної рідини', 'base_price': 600, 'hours': 1},
            {'category': 'Рульове управління', 'name': 'Діагностика керма', 'description': 'Діагностика системи рульового управління', 'base_price': 400, 'hours': 0.5},
            {'category': 'Рульове управління', 'name': 'Заміна пыльников', 'description': 'Заміна пыльників рульових тяг', 'base_price': 400, 'hours': 0.5},
            
            {'category': 'Скло та світло', 'name': 'Заміна лобового скла', 'description': 'Заміна лобового скла', 'base_price': 2500, 'hours': 2},
            {'category': 'Скло та світло', 'name': 'Заміна заднього скла', 'description': 'Заміна заднього скла', 'base_price': 2000, 'hours': 2},
            {'category': 'Скло та світло', 'name': 'Заміна бічного скла', 'description': 'Заміна бічного скла', 'base_price': 1200, 'hours': 1},
            {'category': 'Скло та світло', 'name': 'Регулювання фар', 'description': 'Регулювання напрямку світла фар', 'base_price': 400, 'hours': 0.5},
            {'category': 'Скло та світло', 'name': 'Заміна ламп', 'description': 'Заміна ламп освітлення', 'base_price': 200, 'hours': 0.5},
            {'category': 'Скло та світло', 'name': 'Заміна блоку розжарення', 'description': 'Заміна блоку розжарення ксенону', 'base_price': 1500, 'hours': 1.5},
            {'category': 'Скло та світло', 'name': 'Полірування фар', 'description': 'Полірування пошкоджених фар', 'base_price': 800, 'hours': 1.5},
            {'category': 'Скло та світло', 'name': 'Встановлення LED', 'description': 'Встановлення LED ламп', 'base_price': 600, 'hours': 1},
            {'category': 'Скло та світло', 'name': 'Ремонт омивача', 'description': 'Ремонт системи омивача скла', 'base_price': 500, 'hours': 1},
            {'category': 'Скло та світло', 'name': 'Заміна двірників', 'description': 'Заміна щіток двірників', 'base_price': 300, 'hours': 0.5},
            
            {'category': 'ТО та діагностика', 'name': 'Комплексна діагностика', 'description': 'Повна діагностика автомобіля', 'base_price': 1000, 'hours': 2},
            {'category': 'ТО та діагностика', 'name': 'ТО-1 (масло, фільтри)', 'description': 'Перше технічне обслуговування', 'base_price': 1500, 'hours': 2},
            {'category': 'ТО та діагностика', 'name': 'ТО-2 (масло, фільтри, рідини)', 'description': 'Друге технічне обслуговування', 'base_price': 2500, 'hours': 3},
            {'category': 'ТО та діагностика', 'name': 'Діагностика підвіски', 'description': 'Комплексна діагностика підвіски', 'base_price': 600, 'hours': 1},
            {'category': 'ТО та діагностика', 'name': 'Діагностика гальм', 'description': 'Комплексна діагностика гальмівної системи', 'base_price': 500, 'hours': 1},
            {'category': 'ТО та діагностика', 'name': 'Діагностика двигуна', 'description': 'Діагностика двигуна та ЕБУ', 'base_price': 700, 'hours': 1.5},
            {'category': 'ТО та діагностика', 'name': 'Огляд перед покупкою', 'description': 'Повний огляд автомобіля перед купівлею', 'base_price': 1500, 'hours': 3},
            {'category': 'ТО та діагностика', 'name': 'Заміна охолоджуючої рідини', 'description': 'Заміна антифризу', 'base_price': 900, 'hours': 1.5},
            {'category': 'ТО та діагностика', 'name': 'Заміна гальмівної рідини', 'description': 'Заміна гальмівної рідини DOT', 'base_price': 500, 'hours': 1},
            {'category': 'ТО та діагностика', 'name': 'Заміна рідини ГУР', 'description': 'Заміна рідини гідропідсилювача', 'base_price': 600, 'hours': 1},
            {'category': 'ТО та діагностика', 'name': 'Заміна мастила в АКПП', 'description': 'Заміна мастила в автоматичній КПП', 'base_price': 1500, 'hours': 2},
            {'category': 'ТО та діагностика', 'name': 'Чип-тюнінг', 'description': 'Оптимізація прошивки двигуна', 'base_price': 4000, 'hours': 4},
            
            {'category': 'Додаткові послуги', 'name': 'Евакуатор', 'description': 'Послуги евакуатора', 'base_price': 800, 'hours': 1},
            {'category': 'Додаткові послуги', 'name': 'Підбір запчастин', 'description': 'Підбір оригінальних та аналогових запчастин', 'base_price': 0, 'hours': 0},
            {'category': 'Додаткові послуги', 'name': 'Встановлення запчастин', 'description': 'Монтаж придбаних запчастин', 'base_price': 500, 'hours': 1},
            {'category': 'Додаткові послуги', 'name': 'Страхування', 'description': 'Оформлення страховки ОСАГО та КАСКО', 'base_price': 0, 'hours': 0},
            {'category': 'Додаткові послуги', 'name': 'Тест-драйв', 'description': 'Організація тест-драйву', 'base_price': 500, 'hours': 1},
            {'category': 'Додаткові послуги', 'name': 'Транспортування авто', 'description': 'Доставка автомобіля', 'base_price': 1000, 'hours': 2},
            {'category': 'Додаткові послуги', 'name': 'Зняття з обліку', 'description': 'Допомога в знятті з обліку', 'base_price': 500, 'hours': 1},
            {'category': 'Додаткові послуги', 'name': 'Постановка на облік', 'description': 'Допомога в постановці на облік', 'base_price': 500, 'hours': 1},
            {'category': 'Додаткові послуги', 'name': 'Виїздний ремонт', 'description': 'Ремонт автомобіля на місці', 'base_price': 1000, 'hours': 1},
            {'category': 'Додаткові послуги', 'name': 'Шиномонтаж', 'description': 'Зняття та встановлення коліс', 'base_price': 800, 'hours': 1.5},
            {'category': 'Додаткові послуги', 'name': 'Балансування', 'description': 'Балансування коліс', 'base_price': 400, 'hours': 1},
            {'category': 'Додаткові послуги', 'name': 'Сезонне зберігання шин', 'description': 'Зберігання шин', 'base_price': 500, 'hours': 0},
            {'category': 'Додаткові послуги', 'name': 'Ротація шин', 'description': 'Перестановка коліс', 'base_price': 300, 'hours': 0.5},
            {'category': 'Додаткові послуги', 'name': 'Налаштування запалювання', 'description': 'Налаштування кута випередження запалювання', 'base_price': 500, 'hours': 1},
            {'category': 'Додаткові послуги', 'name': 'Промивка системи охолодження', 'description': 'Промивка системи охолодження', 'base_price': 1000, 'hours': 2},
            {'category': 'Додаткові послуги', 'name': 'Промивка інжектора', 'description': 'Промивка інжекторної системи', 'base_price': 1200, 'hours': 2},
            
            {'category': 'Запчастини', 'name': 'Підбір запчастин', 'description': 'Підбір оригінальних та аналогових запчастин', 'base_price': 0, 'hours': 0},
            {'category': 'Запчастини', 'name': 'Встановлення запчастин', 'description': 'Монтаж придбаних запчастин', 'base_price': 500, 'hours': 1},
        ]
        
        for svc_data in services_data:
            try:
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
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Skipping service {svc_data["name"]}: {e}'))
        
        self.stdout.write(self.style.SUCCESS(f'Created services'))
        
        brands_models = [
            {'brand': 'Toyota', 'models': ['Corolla', 'Camry', 'RAV4', 'Land Cruiser', 'Highlander', 'Prius', 'C-HR', 'Yaris', 'Avensis', 'Verso', 'Tacoma', 'Tundra', '4Runner', 'Sequoia', 'Celica', 'Supra', 'GT86', 'Aqua', 'Sienna', 'Venza']},
            {'brand': 'BMW', 'models': ['3 Series', '5 Series', '7 Series', 'X3', 'X5', 'X7', 'X1', 'X6', 'M3', 'M5', 'X2', 'X4', '8 Series', 'Z4', 'i3', 'i4', 'iX', 'iX3', 'M4', 'M8']},
            {'brand': 'Mercedes-Benz', 'models': ['C-Class', 'E-Class', 'S-Class', 'GLC', 'GLE', 'GLS', 'A-Class', 'B-Class', 'CLA', 'GLA', 'G-Class', 'CLS', 'SL', 'AMG GT', 'EQC', 'EQS', 'V-Class', 'X-Class', 'Citan']},
            {'brand': 'Audi', 'models': ['A3', 'A4', 'A6', 'A8', 'Q3', 'Q5', 'Q7', 'Q8', 'TT', 'R8', 'Q2', 'Q4 e-tron', 'A5', 'A7', 'e-tron', 'e-tron GT', 'RS3', 'RS6', 'RS7', 'SQ5']},
            {'brand': 'Volkswagen', 'models': ['Golf', 'Passat', 'Tiguan', 'Polo', 'Touareg', 'Arteon', 'Jetta', 'T-Roc', 'Caddy', 'Amarok', 'ID.3', 'ID.4', 'ID.5', 'Multivan', 'Transporter', 'Caravelle', 'Teramont', 'Atlas', 'Taos', 'Taigo']},
            {'brand': 'Ford', 'models': ['Focus', 'Mondeo', 'Kuga', 'EcoSport', 'Explorer', 'Mustang', 'Fiesta', 'Ranger', 'Edge', 'Transit', 'Puma', 'Bronco', 'Maverick', 'Galaxy', 'S-Max', 'Kuga', 'Escape', 'Fusion', 'Flex', 'Taurus']},
            {'brand': 'Honda', 'models': ['Civic', 'Accord', 'CR-V', 'HR-V', 'Pilot', 'Odyssey', 'Jazz', 'Insight', 'Ridgeline', 'FR-V', 'City', 'BR-V', 'HR-V', 'WR-V', 'CR-Z', 'S2000', 'NSX', 'Element', 'Pilot', 'Passport']},
            {'brand': 'Hyundai', 'models': ['Elantra', 'Sonata', 'Tucson', 'Santa Fe', 'Creta', 'Kona', 'Palisade', 'Starex', 'Accent', 'Ioniq', 'Venue', 'Bayon', 'Nexo', 'Genesis G70', 'Genesis G80', 'Genesis G90', 'Strix', 'Tucson N Line', 'Ioniq 5', 'Ioniq 6']},
            {'brand': 'Kia', 'models': ['Optima', 'Forte', 'Sportage', 'Sorento', 'Telluride', 'Stonic', 'Ceed', 'Rio', 'Carnival', 'Seltos', 'Niro', 'EV6', 'EV9', 'K5', 'K8', 'Soul', 'Stinger', 'Mohave', 'Ray', 'Pride']},
            {'brand': 'Nissan', 'models': ['Altima', 'Maxima', 'Rogue', 'Pathfinder', 'Murano', 'Qashqai', 'Juke', 'Leaf', 'X-Trail', 'Armada', 'Frontier', 'Titan', 'Z', 'Ariya', 'Kicks', 'Sentra', 'Versa', 'Micra', 'Navara', 'Patrol']},
            {'brand': 'Mazda', 'models': ['Mazda3', 'Mazda6', 'CX-5', 'CX-9', 'CX-30', 'MX-5', 'CX-3', 'CX-50', 'MX-30', 'RX-8', 'CX-60', 'CX-90', 'CX-70', 'CX-80', 'Mazda2', 'BT-50', 'CX-4', 'Atenza', 'Demio', 'Biante']},
            {'brand': 'Volvo', 'models': ['S60', 'S90', 'V60', 'V90', 'XC40', 'XC60', 'XC90', 'XC70', 'S80', 'V40', 'V50', 'V90 Cross Country', 'S90 Recharge', 'XC60 Recharge', 'XC90 Recharge', 'C40', 'EX90', 'EX30', 'EM90']},
            {'brand': 'Porsche', 'models': ['911', 'Cayenne', 'Macan', 'Panamera', 'Taycan', 'Cayman', 'Boxster', '718 Cayman', '718 Boxster', 'Taycan Cross Turismo', 'Taycan Sport Turismo', '911 GT3', '911 Turbo', '911 GT2 RS', 'Cayenne Coupe', 'Macan T']},
            {'brand': 'Lexus', 'models': ['ES', 'IS', 'GS', 'LS', 'RX', 'NX', 'LX', 'UX', 'GX', 'LC', 'RC', 'SC', 'LFA', 'NX Overtrail', 'RZ', 'TX', 'LM', 'UX300e', 'LS500h', 'RX500h']},
            {'brand': 'Subaru', 'models': ['Outback', 'Forester', 'Impreza', 'Legacy', 'XV', 'BRZ', 'WRX', 'Crosstrek', 'Ascent', 'Solterra', 'Tribeca', 'Baja', 'SVX', 'Justy', 'Dex', 'Exiga', 'Lucra', 'Pleo', 'Sambar', 'Stella']},
            {'brand': 'Mitsubishi', 'models': ['Outlander', 'Pajero', 'Lancer', 'Eclipse Cross', 'ASX', 'Montero', 'Space Star', 'Attrage', 'Xpander', 'L200', 'Lancer Evolution', 'Pajero Sport', 'Pajero IO', 'Minica', 'Town BOX', 'i-MiEV', 'eK space', 'Delica', 'Challenger', 'Endeavor']},
            {'brand': 'Peugeot', 'models': ['208', '308', '508', '2008', '3008', '5008', 'Partner', 'Rifter', 'Traveller', 'Boxer', '206', '207', '307', '407', '4007', '4008', '5007', 'Ion', 'e-208', 'e-2008']},
            {'brand': 'Renault', 'models': ['Clio', 'Megane', 'Talisman', 'Kadjar', 'Koleos', 'Arkana', 'Duster', 'Sandero', 'Logan', 'Trafic', 'Kangoo', 'Espace', 'Scenic', 'Grand Scenic', 'Captur', 'Austral', 'Rafale', 'Express', 'Master', 'ZOE']},
            {'brand': 'Citroen', 'models': ['C3', 'C4', 'C5', 'C5 Aircross', 'C3 Aircross', 'Berlingo', 'Jumpy', 'SpaceTourer', 'DS3', 'DS7', 'C1', 'C-Elysee', 'C4 Picasso', 'C4 Spacetourer', 'Grand C4 Picasso', 'C5 X', 'Oli', 'e-C4', 'Ami']},
            {'brand': 'Chery', 'models': ['Tiggo 4', 'Tiggo 7', 'Tiggo 8', 'Exeed TXL', 'Omoda C5', 'Arrizo 8', 'Tiggo 2', 'Bonus', 'Very', 'M11', 'Tiggo 3', 'Tiggo 5', 'Tiggo 5x', 'Tiggo 7 Pro', 'Tiggo 8 Pro', 'Tiggo 8 Pro Max', 'Exeed VX', 'Exeed LX', 'Exeed HS']},
            {'brand': 'Geely', 'models': ['Coolray', 'Atlas', 'Emgrand', 'Monjaro', 'Okavango', 'Tugella', 'Preface', 'Galaxy L6', 'Galaxy L7', 'Galaxy L9', 'Emgrand EV', 'Emgrand EC7', 'Emgrand GS', 'Emgrand EV Pro', 'Geometry A', 'Geometry C', 'Volvo EX30', 'Polestar 2']},
            {'brand': 'Skoda', 'models': ['Octavia', 'Fabia', 'Superb', 'Kodiaq', 'Karoq', 'Kamiq', 'Scala', 'Rapid', 'Enyaq', 'Enyaq Coupe', 'Yeti', 'Roomster', 'Citigo', 'Octavia RS', 'Superb Scout', 'Kodiaq RS', 'Kamiq Monte Carlo', 'Scala Monte Carlo', 'Octavia Monte Carlo']},
            {'brand': 'Opel', 'models': ['Astra', 'Corsa', 'Insignia', 'Mokka', 'Crossland', 'Grandland', 'Zafira', 'Vivaro', 'Combo', 'Movano', 'Astra GTC', 'Astra OPC', 'Corsa OPC', 'Insignia OPC', 'Mokka-e', 'Combo-e', 'Zafira-e Life', 'Grandland X Hybrid', 'Corsa-e']},
            {'brand': 'Seat', 'models': ['Leon', 'Arona', 'Ateca', 'Tarraco', 'Ibiza', 'Alhambra', 'Arona XPERIENCE', 'Leon Cupra', 'Leon ST', 'Leon FR', 'Ateca FR', 'Tarraco XPERIENCE', 'Ibiza FR', 'Alhambra XPERIENCE', 'Leon e-Hybrid', 'Arona e-Hybrid', 'Cupra Formentor', 'Cupra Leon', 'Cupra Ateca', 'Cupra Born']},
            {'brand': 'Suzuki', 'models': ['Vitara', 'SX4', 'Jimny', 'Swift', 'Baleno', 'Ciaz', 'Ertiga', 'Ignis', 'S-Cross', 'Across', 'Vitara S', 'Swift Sport', 'Jimny Sierra', 'Carry', 'APV', 'Liana', 'Grand Vitara', 'XL7', 'Escudo', 'Kizashi']},
            {'brand': 'Daewoo', 'models': ['Lanos', 'Nubira', 'Leganza', 'Matiz', 'Tacuma', 'Evanda', 'Gentra', 'Kalos', 'Lacetti', 'Malibu', 'Optra', 'Sonic', 'Spark', 'Trax', 'Volt', 'Essentix', 'Tosca', 'Winstorm', 'Captiva', 'Equinox']},
            {'brand': 'SsangYong', 'models': ['Tivoli', 'XLV', 'Korando', 'Rexton', 'Actyon', 'Stavic', 'Rodius', 'Kyron', 'Rexton Sports', 'Musso', 'Musso Grand', 'Tivoli Air', 'Torres', 'Torres EVX', 'Rexton EV', 'SsangYong e-SUV', 'Chairman', 'Family', '程s']},
            {'brand': 'Chevrolet', 'models': ['Cruze', 'Malibu', 'Impala', 'Camaro', 'Corvette', 'Tahoe', 'Suburban', 'Traverse', 'Equinox', 'Trax', 'Blazer', 'Colorado', 'Silverado', 'Sonic', 'Spark', 'Volt', 'Bolt', 'Express', 'Avalanche', 'TrailBlazer']},
            {'brand': 'Jeep', 'models': ['Wrangler', 'Grand Cherokee', 'Cherokee', 'Compass', 'Renegade', 'Gladiator', 'Wagoneer', 'Grand Wagoneer', 'Compass 4xe', 'Wrangler 4xe', 'Grand Cherokee 4xe', 'Patriot', 'Liberty', 'Commander', 'Grand Cherokee SRT', 'Wrangler Unlimited', 'Cherokee Trailhawk', 'Compass Trailhawk', 'Renegade Trailhawk', 'Wrangler Rubicon']},
            {'brand': 'Land Rover', 'models': ['Range Rover', 'Range Rover Sport', 'Range Rover Velar', 'Range Rover Evoque', 'Discovery', 'Discovery Sport', 'Defender', 'Freelander', 'Series I', 'Series II', 'Series III', 'Range Rover Sport SVR', 'Range Rover SVR', 'Discovery HSE', 'Defender 90', 'Defender 110', 'Defender 130', 'Range Rover Electric', 'Evoque Convertible']},
            {'brand': 'Tesla', 'models': ['Model S', 'Model 3', 'Model X', 'Model Y', 'Model S Plaid', 'Model X Plaid', 'Cybertruck', 'Roadster', 'Semi', 'Model 3 Long Range', 'Model 3 Performance', 'Model Y Long Range', 'Model Y Performance', 'Model Y Performance', 'Model X Long Range', 'Model S Long Range', 'Model S Performance', 'Cybertruck Tri-Motor', 'Cybertruck Dual-Motor']},
            {'brand': 'Dodge', 'models': ['Charger', 'Challenger', 'Durango', 'Journey', 'Journey Crossroad', 'Nitro', 'Ram', 'Ram 1500', 'Ram 2500', 'Ram 3500', 'Charger SRT', 'Challenger SRT', 'Durango SRT', 'Charger Hellcat', 'Challenger Hellcat', 'Ram TRX', 'Viper', 'Dart', 'Avenger', 'Caliber']},
            {'brand': 'Chrysler', 'models': ['300', 'Pacifica', 'Voyager', 'Town & Country', 'Sebring', '200', 'PT Cruiser', 'Crossfire', 'Aspen', 'Concorde', 'LHS', 'Cirrus', 'Conquest', 'Prowler', 'Delta', 'Ypsilon', 'Flavia', 'Thema', 'Thesis', '300C']},
            {'brand': 'Acura', 'models': ['MDX', 'RDX', 'TLX', 'ILX', 'NSX', 'RLX', 'RL', 'TL', 'TSX', 'ZDX', 'RDX PMC', 'MDX PMC', 'TLX Type S', 'ILX A-Spec', 'RDX A-Spec', 'MDX A-Spec', 'NSX Type R', 'Precision Concept', 'Type S Concept']},
            {'brand': 'Infiniti', 'models': ['Q50', 'Q60', 'Q70', 'QX50', 'QX55', 'QX60', 'QX70', 'QX80', 'Q40', 'Q30', 'QX30', 'EX35', 'EX37', 'FX35', 'FX37', 'FX50', 'G35', 'G37', 'M35', 'M37']},
            {'brand': 'Alfa Romeo', 'models': ['Giulia', 'Stelvio', 'Tonale', '4C', '8C Competizione', 'Giulietta', 'MiTo', '159', 'Brera', 'Spider', 'GT', 'GTA', 'Alfetta', '75', '90', '164', '166', 'Spider Duetto', 'Giulia Quadrifoglio', 'Stelvio Quadrifoglio']},
            {'brand': 'Fiat', 'models': ['500', '500L', '500X', 'Panda', 'Tipo', 'Doblo', 'Ducato', 'Talento', 'Fullback', '124 Spider', '500 Abarth', '500X Abarth', 'Panda Abarth', 'Tipo Abarth', 'Doblo Cargo', 'Ducato Maxi', 'Fullback Cross', '500 Hybrid', '500e', 'Panda Hybrid']},
            {'brand': 'Mini', 'models': ['Cooper', 'Cooper S', 'Cooper SE', 'Cooper JCW', 'Countryman', 'Countryman SE', 'Clubman', 'Paceman', 'Convertible', 'Roadster', 'Coupe', 'Cooper Clubman', 'Cooper Works', 'Cooper S Clubman', 'Countryman JCW', 'John Cooper Works GP', 'Mini Electric', 'Mini Aceman']},
            {'brand': 'Jaguar', 'models': ['F-PACE', 'E-PACE', 'I-PACE', 'F-TYPE', 'XE', 'XF', 'XJ', 'XK', 'X-Type', 'S-Type', 'XKR', 'XKR-S', 'F-TYPE R', 'F-TYPE SVR', 'I-PACE HSE', 'I-PACE SE', 'F-PACE SVR', 'E-PACE R-Dynamic', 'XE R-Dynamic']},
            {'brand': 'Buick', 'models': ['Enclave', 'Encore', 'Encore GX', 'Envision', 'LaCrosse', 'Regal', 'Verano', 'Cascada', 'Regal Sportback', 'Regal TourX', 'Envoy', 'Rainier', 'Rendezvous', 'Terraza', 'Lucerne', 'Park Avenue', 'LeSabre', 'Century', 'Electra']},
            {'brand': 'GMC', 'models': ['Sierra', 'Terrain', 'Acadia', 'Yukon', 'Canyon', 'Savana', 'Acadia Limited', 'Envoy', 'Jimmy', 'Syclone', 'Typhon', 'Sonoma', 'Sierra HD', 'Yukon XL', 'Sierra Denali', 'Terrain Denali', 'Yukon Denali', 'Sierra AT4X', 'Yukon AT4']},
            {'brand': 'Cadillac', 'models': ['Escalade', 'XT4', 'XT5', 'XT6', 'CT4', 'CT5', 'CT6', 'ATS', 'CTS', 'XTS', 'SRX', 'XT5', 'Escalade ESV', 'Escalade V', 'CT4-V', 'CT5-V', 'CT6-V', 'Lyriq', 'Celestiq', 'Optiq']},
            {'brand': 'Lincoln', 'models': ['Navigator', 'Aviator', 'Corsair', 'Nautilus', 'MKC', 'MKS', 'MKT', 'MKZ', 'MKX', 'Continental', 'Town Car', 'Navigator L', 'Aviator Grand Touring', 'Corsair Grand Touring', 'Nautilus Reserve', 'MKC Reserve', 'MKZ Reserve', 'Continental Reserve', 'Zephyr']},
            {'brand': 'Audi UK', 'models': ['A1', 'A2', 'A4 Allroad', 'A6 Allroad', 'Q1', 'SQ2', 'SQ5', 'SQ7', 'SQ8', 'RS Q3', 'RS Q5', 'RS Q8', 'R8 V10', 'R8 V10 Plus', 'TT RS', 'RS3', 'RS4', 'RS6', 'RS7']},
            {'brand': 'Toyota UK', 'models': ['Aygo', 'Urban Cruiser', 'Urban Cruiser Hybrid', 'Proace', 'Proace City', 'Hilux', 'Proace Verso', 'Corolla Touring Sports', 'RAV4 Hybrid', 'RAV4 Plug-in Hybrid', 'Camry Hybrid', 'Prius Plug-in', 'Yaris Cross', 'Yaris Hybrid', 'GR86', 'GR Supra', 'GR Corolla', 'Corolla Cross Hybrid']},
            {'brand': 'Peugeot UK', 'models': ['108', '208', '308 SW', '508 SW', '2008', '3008', '5008', 'Rifter', 'Partner Pro', 'e-Expert', 'e-Boxer', '508 PSE', 'e-208 PSE', '3008 Hybrid', '4008 Hybrid', '5008 Hybrid', '108 Top', '208 GT', '308 GT']},
            {'brand': 'Renault UK', 'models': ['Twingo', 'Clio', 'Captur', 'Arkana', 'Koleos', 'Trafic Passenger', 'Master Passenger', 'ZOE', 'Twingo Z.E.', 'Kangoo Z.E.', 'Master Z.E.', 'Alpine A110', 'Alpine A110 S', 'Arkana E-Tech', 'Captur E-Tech', 'Megane E-Tech', 'ZOE Iconic', 'ZOE Intens']},
            {'brand': 'Nissan UK', 'models': ['Pulsar', 'Note', 'Note e-POWER', 'Micra', 'Juke', 'Qashqai', 'X-Trail', 'Leaf', 'e-NV200', 'NV200 Evalia', 'Navara', 'Patrol', 'GT-R', '370Z', 'Juke N-Style', 'Qashqai N-Design', 'X-Trail N-Design', 'Leaf e+', 'Ariya']},
            {'brand': 'Volkswagen UK', 'models': ['Up', 'Polo', 'Golf', 'Golf Estate', 'Golf GTI', 'Golf R', 'Passat Estate', 'Passat GTE', 'Arteon Shooting Brake', 'T-Roc', 'T-Roc R', 'Tiguan', 'Tiguan Allspace', 'Touareg', 'Sharan', 'Caravelle', 'Multivan', 'ID.Buzz', 'ID.3 Pro']},
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
