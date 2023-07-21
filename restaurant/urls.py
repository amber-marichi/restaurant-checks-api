from django.urls import path, include
from rest_framework.routers import DefaultRouter

from restaurant.views import (
    CheckViewSet,
    PrinterViewSet,
    add_new_order,
)


router = DefaultRouter()
router.register("printers", PrinterViewSet, basename="printers")
router.register("checks", CheckViewSet, basename="checks")

urlpatterns = [
    path("order/", add_new_order, name="order"),
    path("", include(router.urls)),
]

app_name = "printing"
