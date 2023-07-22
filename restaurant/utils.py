import base64
import json
import requests
from os import path

from django.conf import settings
from django.template.loader import render_to_string

from restaurant.models import Check


def get_pdf_response(html_string: str) -> bytes:
    payload = base64.b64encode(html_string.encode()).decode()
    data = {
        "contents": payload,
    }

    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(settings.PDF_URL, data=json.dumps(data), headers=headers)
    return response.content


def save_file(file_name: str, html_string: str) -> str:
    pdf_response = get_pdf_response(html_string)
    full_path = path.join(settings.MEDIA_ROOT, "pdf", file_name)
    with open(full_path, "wb") as writer:
        writer.write(pdf_response)
    return full_path


def create_pdf(check_id: int) -> int:
    check = Check.objects.get(id=check_id)
    order_id = check.order.get("order_id")
    check_type = check.type
    file_name = f"{order_id}_{check_type}.pdf"

    context = {"check_data": check}
    html_string = render_to_string("restaurant/check.html", context)

    file_path = save_file(file_name, html_string)
    relative_path = path.relpath(file_path, start=settings.MEDIA_ROOT)
    check.pdf_file = "pdf/" + path.basename(relative_path)
    check.status = Check.READY
    check.save()
    return check.printer_id.pk


def print_ready_checks(printer_id: int) -> None:
    ready_checks = Check.objects.filter(printer_id=printer_id, status=Check.READY)

    for check in ready_checks:
        check.status = Check.PRINTED
        check.save()
        print(f"{check} is sent for printing!")
