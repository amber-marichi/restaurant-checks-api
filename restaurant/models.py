from django.db import models


PRINT_TYPE_CHOICES = [
    ("CLT", "client"),
    ("KTN", "kitchen"),
]


class Printer(models.Model):
    name = models.CharField(max_length=200)
    api_key = models.CharField(max_length=200, unique=True)
    check_type = models.CharField(max_length=3, choices=PRINT_TYPE_CHOICES)
    point_id = models.IntegerField()

    def __str__(self) -> str:
        return self.name + self.check_type.value


class Check(models.Model):
    CHECK_STATUS_CHOICES = [
        ("N", "new"),
        ("R", "ready"),
        ("P", "printed")
    ]

    printer_id = models.ForeignKey(to=Printer, on_delete=models.CASCADE)
    order_type = models.CharField(max_length=3, choices=PRINT_TYPE_CHOICES)
    oder = models.JSONField(blank=True)
    status = models.CharField(max_length=1, choices=CHECK_STATUS_CHOICES)
    pdf_file = models.FileField(blank=True, upload_to="pdf")

    def __str__(self) -> str:
        return str(self.id)
