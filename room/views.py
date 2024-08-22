from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import RoomRate, OverriddenRoomRate, Discount, DiscountRoomRate
from .serializers import (
    RoomRateSerializer, OverriddenRoomRateSerializer, 
    DiscountSerializer, DiscountRoomRateSerializer
)
from django.db.models import Min, F
from rest_framework.filters import SearchFilter

class CustomViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "status": True,
                "message": "Data created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": False,
            "message": "Missing fields",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({
                "status": True,
                "message": "Data updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": False,
            "message": "Missing fields",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "status": True,
            "message": "Data fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": True,
            "message": "Data fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "status": True,
            "message": "Data deleted successfully",
            "data": {}
        }, status=status.HTTP_204_NO_CONTENT)

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

                discount = DiscountRoomRate.objects.filter(
                    room_rate=rate
                ).aggregate(
                    max_discount=Min('discount__discount_value')
                )

                if discount['max_discount']:
                    final_rate = overridden_rate['lowest_rate'] - discount['max_discount']
                else:
                    final_rate = overridden_rate['lowest_rate']

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
