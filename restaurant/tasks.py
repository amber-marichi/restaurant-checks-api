from celery import chain, shared_task

from restaurant.utils import create_pdf, print_ready_checks


@shared_task()
def process_pdf_check(check_id: int) -> None:
    print(f"processing check for order {check_id}")
    printer_id = create_pdf(check_id)
    print(f"order {check_id} file is ready! chaining to printer {printer_id}")
    chain(printer_checks_status.s(printer_id).set(countdown=2)).apply_async()


@shared_task()
def printer_checks_status(printer_id: int) -> None:
    print_ready_checks(printer_id)
