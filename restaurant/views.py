from typing import Type

from django.http import HttpRequest, HttpResponse

from rest_framework import  mixins, status, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from restaurant.models import Check, Printer
from restaurant.serializers import (
    CheckSerializer,
    CheckListSerializer,
    PrinterSerializer,
    PrinterCreateSerializer,
)
from restaurant.tasks import process_pdf_check


class CheckViewSet(
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Check.objects.select_related("printer_id")
    serializer_class = CheckListSerializer


class PrinterViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Printer.objects.all()

    def get_serializer_class(self) -> Type[serializers.Serializer]:
    
        if self.action == "create":
            return PrinterCreateSerializer

        return PrinterSerializer


@api_view(["POST"])
def add_new_order(request: HttpRequest) -> HttpResponse:
    serializer = CheckSerializer(data=request.data)
    if serializer.is_valid():

        order_data = serializer.validated_data.get("order")
        printers = Printer.objects.filter(point_id=order_data["location_id"])

        for printer in printers:
            new_check = Check.objects.create(
                printer_id=printer,
                type=printer.check_type,
                order=order_data,
            )
            process_pdf_check.delay(new_check.id)

        return Response("Checks created successfully.", status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
