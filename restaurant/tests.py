from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

from restaurant.models import Printer, Check, PrintType


URL_CREATE_ORDER = reverse("restaurant:order")

class CheckCreationTests(APITestCase):
    def setUp(self) -> None:
        self.printer1kit = Printer.objects.create(
            name="printer 12 - kitchen",
            check_type=PrintType.KITCHEN,
            point_id=12
        )
        self.printer1cli = Printer.objects.create(
            name="printer 12 - client",
            check_type=PrintType.CLIENT,
            point_id=12
        )
        self.printer1kit = Printer.objects.create(
            name="printer 21 - kitchen",
            check_type=PrintType.KITCHEN,
            point_id=21
        )
    
    def test_check_point_two_printers(self) -> None:
        data = {
            "order": {
              "order_id": 111,
              "location_id": 12,
              "meal": 12,
              "drink": 5,
              "dessert": 16
            }
        }

        response = self.client.post(URL_CREATE_ORDER, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Check.objects.filter(order=data["order"]).count(), 2)
    
    def test_check_point_one_printer(self) -> None:
        data = {
            "order": {
              "order_id": 222,
              "location_id": 21,
              "meal": 12,
              "drink": 5,
              "dessert": 16
            }
        }

        response = self.client.post(URL_CREATE_ORDER, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Check.objects.filter(order=data["order"]).count(), 1)
    
    def test_check_point_no_printer(self) -> None:
        data = {
            "order": {
              "order_id": 3535,
              "location_id": 44,
              "meal": 12,
              "drink": 5,
              "dessert": 16
            }
        }

        response = self.client.post(URL_CREATE_ORDER, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_check_already_created(self) -> None:
        data = {
            "order": {
              "order_id": 3131,
              "location_id": 21,
              "meal": 12,
              "drink": 5,
              "dessert": 16
            }
        }

        response = self.client.post(URL_CREATE_ORDER, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        second_response = self.client.post(URL_CREATE_ORDER, data, format="json")
        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Check.objects.filter(order=data["order"]).count(), 1)

    def test_check_invalid_order_data(self) -> None:
        wrong_data_no_order = {
            "order": {
              "location_id": 12,
              "meal": 12,
              "drink": 5,
              "dessert": 16
            }
        }
        wrong_data_no_location = {
            "order": {
              "order_id": 4144,
              "meal": 12,
              "drink": 5,
              "dessert": 16
            }
        }

        response = self.client.post(URL_CREATE_ORDER, wrong_data_no_order, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(URL_CREATE_ORDER, wrong_data_no_location, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("restaurant.tasks.process_pdf_check.delay")
    def test_pdf_task_was_triggered(self, mock_tasks) -> None:
        data = {
            "order": {
              "order_id": 111,
              "location_id": 21,
              "meal": 12,
              "drink": 5,
              "dessert": 16
            }
        }

        response = self.client.post(URL_CREATE_ORDER, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(mock_tasks.called)
        check_id = Check.objects.latest("id").id
        mock_tasks.assert_called_once_with(check_id)
