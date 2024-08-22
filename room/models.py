from django.db import models
from utils.config import DECIMAL_PLACES,DISCOUNT_TYPE_CHOICES




class RoomRate(models.Model):
    room_id = models.IntegerField()
    room_name = models.CharField(max_length=100)
    default_rate = models.DecimalField(max_digits=10, decimal_places=DECIMAL_PLACES)

    def __str__(self):
        return self.room_name

class OverriddenRoomRate(models.Model):
    room_rate = models.ForeignKey(RoomRate, related_name="room_rates", on_delete=models.CASCADE)
    overridden_rate = models.DecimalField(max_digits=10, decimal_places=DECIMAL_PLACES)
    stay_date   = models.DateField()
    


    def __str__(self):
        return f"{self.room_rate.room_name} - {self.stay_date}"

class Discount(models.Model):
    discount_name = models.CharField(max_length=255)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=DECIMAL_PLACES)

    def __str__(self):
        return self.discount_name
    

class DiscountRoomRate(models.Model):
    room_rate = models.ForeignKey(RoomRate, related_name="discounted_room_rates", on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.room_rate.room_name} - {self.discount.discount_name}"