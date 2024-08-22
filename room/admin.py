from django.contrib import admin

# Register your models here.


from .models import *



admin.site.register(RoomRate)
admin.site.register(OverriddenRoomRate)
admin.site.register(Discount)
admin.site.register(DiscountRoomRate)




