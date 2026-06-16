Django Simple Blog API

A RESTful Blog API built with Django and Django REST Framework featuring user authentication, post management, filtering, pagination, background task processing with Celery, and interactive API documentation.

Features

- User registration
- Token-based authentication
- Blog post CRUD operations
- Pagination support
- Filtering with django-filter
- Celery background tasks
- Redis message broker
- Swagger API documentation
- ReDoc API documentation
- Automated tests for serializers and views
- Dockerized environment

Tech Stack

Backend

- Django 6
- Django REST Framework
- Django Filter

Async Processing

- Celery
- Redis

Documentation

- Swagger UI
- ReDoc
- drf-yasg

DevOps

- Docker
- Docker Compose

Testing

- Django Test Framework

---

Installation

Clone Repository

git clone https://github.com/MahdiKhanmohammadi/django_simple_blog.git
cd django_simple_blog

Create Virtual Environment

python -m venv venv

Linux / Mac:

source venv/bin/activate

Windows:

venv\Scripts\activate

Install Dependencies

pip install -r requirements.txt

Apply Migrations

python manage.py migrate

Create Superuser

python manage.py createsuperuser

Run Server

python manage.py runserver

---

Docker

Build and run containers:

docker compose up --build

Run in background:

docker compose up -d

Stop containers:

docker compose down

---

Celery

Run worker:

celery -A config worker -l info

Make sure Redis is running before starting Celery.

---

API Documentation

Swagger UI:

/swagger/

ReDoc:

/redoc/

---

Testing

Run all tests:

python manage.py test

Run blog tests:

python manage.py test blog

Run accounts tests:

python manage.py test accounts



---

License

This project is licensed under the MIT License.

---

Author

Mahdi Khanmohammadi

GitHub:
https://github.com/MahdiKhanmohammadi
