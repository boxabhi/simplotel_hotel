from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import RoomRate, OverriddenRoomRate, Discount, DiscountRoomRate
from    .serializers import (
    RoomRateSerializer, OverriddenRoomRateSerializer, 
    DiscountSerializer, DiscountRoomRateSerializer
)
from django.db.models import Min, F
from utils.utils import CustomViewSet
from rest_framework.filters import SearchFilter



class RoomRateViewSet(CustomViewSet):
    queryset = RoomRate.objects.all()
    serializer_class = RoomRateSerializer

class OverriddenRoomRateViewSet(CustomViewSet):
    queryset = OverriddenRoomRate.objects.all()
    serializer_class = OverriddenRoomRateSerializer
    filter_backends = [SearchFilter]
    search_fields = ['room_rate__room_name', 'overridden_rate', 'stay_date']

class DiscountViewSet(CustomViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer

class DiscountRoomRateViewSet(CustomViewSet):
    queryset = DiscountRoomRate.objects.all()
    serializer_class = DiscountRoomRateSerializer

class LowestRateViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            room_ids = request.query_params.get('room_ids')
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')

            if not room_ids:
                return Response({
                    "status": False,
                    "message": "room_ids parameter is required",
                    "data": {}
                }, status=status.HTTP_400_BAD_REQUEST)

            room_id_list = [int(id.strip()) for id in room_ids.split(',')]
            rates = RoomRate.objects.filter(room_id__in=room_id_list)
            lowest_rates = []

            for rate in rates:
                overridden_rate = OverriddenRoomRate.objects.filter(
                    room_rate=rate, stay_date__range=[start_date, end_date]
                ).annotate(
                    final_rate=F('overridden_rate')
                ).aggregate(
                    lowest_rate=Min('final_rate')
                )

                if not overridden_rate['lowest_rate']:
                    overridden_rate = {'lowest_rate': rate.default_rate}

                discounts = DiscountRoomRate.objects.filter(room_rate=rate).select_related('discount')
                max_discount_value = 0

                for discount in discounts:
                    discount_obj = discount.discount
                    if discount_obj.discount_type == 'percentage':
                        discount_value = (discount_obj.discount_value / 100) * overridden_rate['lowest_rate']
                    else:
                        discount_value = discount_obj.discount_value
                    
                    if discount_value > max_discount_value:
                        max_discount_value = discount_value


                final_rate = overridden_rate['lowest_rate'] - max_discount_value


                lowest_rates.append({
                    'room_id': rate.room_id,
                    'room_name': rate.room_name,
                    'final_rate': final_rate,
                    'stay_date': start_date,
                })

            return Response({
                "status": True,
                "message": "Data fetched successfully",
                "data": lowest_rates
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": False,
                "message": f"Something went wrong: {str(e)}",
                "data": {}
            }, status=status.HTTP_400_BAD_REQUEST)
