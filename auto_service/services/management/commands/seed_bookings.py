import random
from datetime import datetime, timedelta

from accounts.models import User
from bookings.models import Booking
from cars.models import CarBrand, CarModel, UserCar
from django.core.management.base import BaseCommand
from django.utils import timezone
from services.models import Service


class Command(BaseCommand):
    help = "Create random bookings for demo purposes"

    def handle(self, *args, **options):
        existing_bookings = Booking.objects.count()
        if existing_bookings > 0:
            self.stdout.write(
                self.style.WARNING(f"Deleting {existing_bookings} existing bookings...")
            )
            Booking.objects.all().delete()

        try:
            client = User.objects.filter(role="CLIENT").first()
            if not client:
                client = User.objects.first()

            cars = list(UserCar.objects.all())
            if not cars:
                self.stdout.write(self.style.ERROR("No cars found. Please run seed_data first."))
                return

            services = list(Service.objects.all())
            if not services:
                self.stdout.write(
                    self.style.ERROR("No services found. Please run seed_data first.")
                )
                return

            service_names = [s.name for s in services]

            if not service_names:
                service_names = [
                    "Заміна моторної оливи",
                    "ТО-1",
                    "ТО-2",
                    "Діагностика",
                    "Заміна гальмівних колодок",
                    "Розвал-сходження",
                    "Заміна амортизаторів",
                    "Заправка кондиціонера",
                    "Заміна повітряного фільтра",
                    "Заміна салонного фільтра",
                    "Заміна гальмівних дисків",
                    "Заміна акумулятора",
                ]

            statuses = ["PENDING", "CONFIRMED", "IN_PROGRESS", "DONE"]

            now = timezone.now()
            bookings_created = 0

            for _ in range(80):
                days_offset = random.randint(-30, 60)
                hour = random.choice([8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18])

                booking_datetime = now + timedelta(days=days_offset, hours=hour)

                if booking_datetime > now:
                    status = random.choice(["PENDING", "CONFIRMED"])
                else:
                    status = random.choice(["CONFIRMED", "IN_PROGRESS", "DONE"])

                car = random.choice(cars)
                service_type = random.choice(service_names)

                booking = Booking.objects.create(
                    client=client,
                    car=car,
                    scheduled_at=booking_datetime,
                    service_type=service_type,
                    status=status,
                    notes=random.choice(["", "Терміново", "Бажано вранці", "Тільки після 14:00"]),
                    total_cost=random.randint(500, 5000),
                )
                bookings_created += 1

            self.stdout.write(self.style.SUCCESS(f"Created {bookings_created} random bookings"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
