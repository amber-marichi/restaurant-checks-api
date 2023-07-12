from rest_framework import serializers

from restaurant.models import Check, Printer


class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = [
            "pk",
            "printer_id",
            "type",
            "order",
            "status",
            "pdf_file",
        ]


class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = [
            "pk",
            "name",
            "api_key",
            "check_type",
            "point_id",
        ]
