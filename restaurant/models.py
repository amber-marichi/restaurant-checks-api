import uuid
from django.db import models


class PrintType(models.TextChoices):
    CLIENT = "CLT"
    KITCHEN = "KIT"


class Printer(models.Model):
    name = models.CharField(max_length=200)
    api_key = models.UUIDField(default=uuid.uuid4, unique=True)
    check_type = models.CharField(max_length=3, choices=PrintType.choices)
    point_id = models.IntegerField()

    def __str__(self) -> str:
        return self.name + " - " + self.check_type


class Check(models.Model):
    NEW = "N"
    READY = "R"
    PRINTED = "P"
    CHECK_STATUS_CHOICES = [
        (NEW, "new"),
        (READY, "ready"),
        (PRINTED, "printed")
    ]

    printer_id = models.ForeignKey(
        to=Printer,
        on_delete=models.CASCADE,
        related_name="checks"
    )
    type = models.CharField(max_length=3, choices=PrintType.choices)
    order = models.JSONField()
    status = models.CharField(
        max_length=1,
        choices=CHECK_STATUS_CHOICES,
        default=CHECK_STATUS_CHOICES[0][0])
    pdf_file = models.FileField(upload_to='pdf/', blank=True)

    def __str__(self) -> str:
        return str(self.id) + " - " + self.type
