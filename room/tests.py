from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import RoomRate, OverriddenRoomRate, Discount, DiscountRoomRate

class LowestRateViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.setup_demo_data()

    def setup_demo_data(self):

        self.room1 = RoomRate.objects.create(
            room_id=101,
            room_name='Single Room',
            default_rate=100.00
        )
        self.room2 = RoomRate.objects.create(
            room_id=102,
            room_name='Double Room',
            default_rate=200.00
        )
        self.room3 = RoomRate.objects.create(
            room_id=103,
            room_name='Suite',
            default_rate=300.00
        )


        today = timezone.now().date()
        self.overridden_rate1 = OverriddenRoomRate.objects.create(
            room_rate=self.room1,
            overridden_rate=90.00,
            stay_date=today
        )
        self.overridden_rate2 = OverriddenRoomRate.objects.create(
            room_rate=self.room2,
            overridden_rate=180.00,
            stay_date=today + timedelta(days=1)
        )


        self.discount1 = Discount.objects.create(
            
            discount_name='Summer Sale',
            discount_type='percentage',
            discount_value=10.00
        )
        self.discount2 = Discount.objects.create(
            
            discount_name='Weekend Discount',
            discount_type='fixed',
            discount_value=20.00
        )


        DiscountRoomRate.objects.create(
            room_rate=self.room1,
            discount=self.discount1
        )
        DiscountRoomRate.objects.create(
            room_rate=self.room2,
            discount=self.discount2
        )

    def test_lowest_rate_endpoint_single_room_id(self):
        response = self.client.get('/api/room/lowest-rates/', {
            'room_ids': '101',
            'start_date': timezone.now().date(),
            'end_date': (timezone.now() + timedelta(days=1)).date()
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['room_id'], 101)

    def test_lowest_rate_endpoint_multiple_room_ids(self):
        response = self.client.get('/api/room/lowest-rates/', {
            'room_ids': '101,102',
            'start_date': timezone.now().date(),
            'end_date': (timezone.now() + timedelta(days=1)).date()
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertGreaterEqual(len(response.data['data']), 2)

    def test_lowest_rate_endpoint_with_no_room_ids(self):
        response = self.client.get('/api/room/lowest-rates/', {
            'start_date': timezone.now().date(),
            'end_date': (timezone.now() + timedelta(days=1)).date()
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], False)
        self.assertEqual(response.data['message'], "room_ids parameter is required")
        self.assertEqual(response.data['data'], {})

    def test_lowest_rate_endpoint_with_invalid_room_ids(self):
        response = self.client.get('/api/room/lowest-rates/', {
            'room_ids': '1,2',
            'start_date': timezone.now().date(),
            'end_date': (timezone.now() + timedelta(days=1)).date()
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertEqual(response.data['data'], [])

    def test_lowest_rate_endpoint_with_discounts(self):
        response = self.client.get('/api/room/lowest-rates/', {
            'room_ids': '101,102',
            'start_date': timezone.now().date(),
            'end_date': (timezone.now() + timedelta(days=1)).date()
        })
       
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)

        data = response.data['data']
        for entry in data:
            if entry['room_id'] == 101:
                self.assertEqual(entry['final_rate'], 90.00 - 10.00)  
            elif entry['room_id'] == 102:
                self.assertEqual(entry['final_rate'], 180.00 - 20.00)  

