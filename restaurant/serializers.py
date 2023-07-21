from rest_framework import serializers

from restaurant.models import Check, Printer


class CheckListSerializer(serializers.ModelSerializer):
    printer = serializers.CharField(source="printer_id.name", read_only=True)
    type = serializers.CharField(source="get_type_display")
    status = serializers.CharField(source="get_status_display")
    class Meta:
        model = Check
        fields = [
            "pk",
            "printer",
            "type",
            "order",
            "status",
            "pdf_file",
        ]


class PrinterSerializer(serializers.ModelSerializer):
    check_type = serializers.CharField(source="get_check_type_display")
    class Meta:
        model = Printer
        fields = [
            "pk",
            "name",
            "api_key",
            "check_type",
            "point_id",
        ]


class PrinterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = [
            "name",
            "check_type",
            "point_id",
        ]


class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = ["order",]

    def validate_order(self, value: any) -> any:
        try:
            location = value.get("location_id")
            order_id = value.get("order_id")
            if not location or not order_id:
                raise serializers.ValidationError("the order must contain location and order id info")
        except (TypeError, AttributeError):
            raise serializers.ValidationError("the order data must be json format")

        existing_checks = Check.objects.filter(order=value)

        if existing_checks.exists():
            raise serializers.ValidationError("check already exists for order", order_id)

        printers = Printer.objects.filter(point_id=location)
        if not printers:
            raise serializers.ValidationError("no printers found for this point")

        return value
