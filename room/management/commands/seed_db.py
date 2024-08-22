from django.core.management.base import BaseCommand
from room.models import RoomRate, OverriddenRoomRate, Discount, DiscountRoomRate
from datetime import date

class Command(BaseCommand):
    help = 'Seed the database with demo data'

    def handle(self, *args, **kwargs):
        
        RoomRate.objects.all().delete()
        OverriddenRoomRate.objects.all().delete()
        Discount.objects.all().delete()
        DiscountRoomRate.objects.all().delete()


        room_rate1 = RoomRate.objects.create(room_id=101, room_name='Deluxe Room', default_rate=200.00)
        room_rate2 = RoomRate.objects.create(room_id=102, room_name='Suite Room', default_rate=300.00)


        overridden_rate1 = OverriddenRoomRate.objects.create(room_rate=room_rate1, overridden_rate=180.00, stay_date=date(2024, 8, 22))
        overridden_rate2 = OverriddenRoomRate.objects.create(room_rate=room_rate2, overridden_rate=280.00, stay_date=date(2024, 8, 23))

        discount1 = Discount.objects.create( discount_name='Summer Sale', discount_type='percentage', discount_value=10)
        discount2 = Discount.objects.create( discount_name='Holiday Discount', discount_type='fixed', discount_value=20.00)

        # Map Room Rates with Discounts
        DiscountRoomRate.objects.create(room_rate=room_rate1, discount=discount1)
        DiscountRoomRate.objects.create(room_rate=room_rate1, discount=discount2)
        DiscountRoomRate.objects.create(room_rate=room_rate2, discount=discount1)

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with demo data'))
