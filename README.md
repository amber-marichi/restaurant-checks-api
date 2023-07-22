# Restaurant check printing api service
The restaurant has several locations throughout the city. Both clients and kitchen stuff want to have their receipts with order details.
The service works to help them by recieving order details, asynchronously generating pdf check files and sending them for printing.

## Features
![arch](https://github.com/amber-marichi/restaurant-checks-api/assets/72259870/6b1f0083-e542-4365-baae-b75b6ca17676)

- The service receives information about a new order, creates checks in the database for all printers of the location specified in the order, and sets asynchronous tasks for generating PDF files for these checks. If there is no printer set for the location an error status is returned. If there is receipts for this order in DB, an error status is returned (the order number is passed).
- An asynchronous worker generates a PDF file from an HTML template with wkhtmltopdf. The file name should look like <order ID>_<check type>.pdf (123456_client.pdf). The files should be stored in the media/pdf folder in the root of the project.
- The task queries for receipts that have already been generated for a specific printer, pdf files that are ready then sent for printing which results in their status change.
- Both Printer and Check models are registered for admin panel with possibility to filter checks by printer, type and status.
- PostgreSQL is used as database, Redis used as task broker.
- docker compose file to easily set up all necessary container for db's and pdf printing

## Setting up project and getting started
Install using GitHUB
```sh
git clone https://github.com/amber-marichi/restaurant-checks-api.git
cd restaurant-checks-api
```

Set up variables
Prepare the .env file using .env.sample provided in project main directory. Change following values accordingly to database name, user name and password. Save file with variables as ".env"
```sh
DJANGO_SECRET_KEY=
DJANGO_DEBUG=1
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
PG_HOST=
PDF_URL=
BROKER_URL=
RESULT_BACKEND_URL=
```

### To run using Docker
!! Docker with docker compose must be installed and ready

Run docker compose command
```sh
docker compose up -d
```
Verify the deployment by navigating to your server address in
your preferred browser.

```sh
127.0.0.1:8000/api
```

### To run locally
!! Python3.8+ with pip should be installed and ready.
PostgreSQL database should be running locally or in Docker with creds corresponding to ones stated in .env file.

1. Create and activate venv:
```sh
python -m venv venv
```

2. Activate environment:

On Mac and Linux:
```sh
source venv/bin/activate
```
On Windows
```sh
venv/Scripts/activate
```

3. Install requirements:

```sh
pip install -r requirements.txt
```

4. Apply migrations

```sh
python manage.py migrate
```

5. Start Celery by running command:
```sh
python -m celery -A core worker -l info
```

6. Start the app:

```sh
python manage.py runserver
```

### To get access to the app
1. After project is up list of available Printers and Checks can be seen by following endpoints:
```sh
http://127.0.0.1:8000/api/printers/
http://127.0.0.1:8000/api/checks/
```
2. To load fixture with few preset points with printers run command (or add new one by "printers" endpoint)
```sh
python manage.py loaddata printer_fixture.json
```
3. Now you are ready to proceed with adding new orders
```sh
http://127.0.0.1:8000/api/order/
```
Passed data should be in json format with present "location_id" and "order_id", i.e.:
```sh
{
  "order": {
    "order_id": 2141,
    "location_id": 3,
    "meal": 25,
    "drink": 13,
    "dessert": 10
  }
}
```
