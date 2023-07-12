from django.contrib import admin

from restaurant.models import Check, Printer


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "printer_id",
        "type",
        "order",
        "status",
        "pdf_file",
    )
    list_filter = (
        "printer_id__name",
        "type",
        "status",
    )


@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "api_key",
        "check_type",
        "point_id",
    )
