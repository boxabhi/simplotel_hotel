from django.urls import path
from .views import (
    RoomRateViewSet, OverriddenRoomRateViewSet, 
    DiscountViewSet, DiscountRoomRateViewSet, LowestRateViewSet
)
from rest_framework.routers import DefaultRouter

# Initialize the router
router = DefaultRouter()
router.register('room-rates', RoomRateViewSet)
router.register('overridden-rates', OverriddenRoomRateViewSet)
router.register('discounts', DiscountViewSet)
router.register('discount-room-rates', DiscountRoomRateViewSet)
router.register('lowest-rates', LowestRateViewSet, basename='lowest-rates')

urlpatterns = [
    path('room-rates/', RoomRateViewSet.as_view({'get': 'list', 'post': 'create'}), name='room-rates-list-create'),
    path('room-rates/<int:pk>/', RoomRateViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='room-rates-detail'),

    path('overridden-rates/', OverriddenRoomRateViewSet.as_view({'get': 'list', 'post': 'create'}), name='overridden-rates-list-create'),
    path('overridden-rates/<int:pk>/', OverriddenRoomRateViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='overridden-rates-detail'),

    path('discounts/', DiscountViewSet.as_view({'get': 'list', 'post': 'create'}), name='discounts-list-create'),
    path('discounts/<int:pk>/', DiscountViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='discounts-detail'),

    path('discount-room-rates/', DiscountRoomRateViewSet.as_view({'get': 'list', 'post': 'create'}), name='discount-room-rates-list-create'),
    path('discount-room-rates/<int:pk>/', DiscountRoomRateViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='discount-room-rates-detail'),

    path('lowest-rates/', LowestRateViewSet.as_view({'get': 'list'}), name='lowest-rates-list'),
]

# Include the router URLs
urlpatterns += router.urls
