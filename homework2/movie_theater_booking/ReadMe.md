Alien Movie Theater Booking — Django + DRF

A RESTful movie-theater booking app built with Django 4.2 and Django REST Framework (DRF).
Users can browse movies, book seats, and view booking history through both HTML pages (Bootstrap) and a JSON API that power the same data.

Features

Models (MVT)

Movie(title, description, release_date, duration, created_at, updated_at)

Seat(seat_number, booking_status, created_at, updated_at)

Booking(movie, seat, user, booking_date, created_at, updated_at)

Data-layer guard: unique_together = ("movie", "seat") + booking logic marks seats as BOOKED.

RESTful API (DRF)

MovieViewSet — full CRUD for movies

SeatViewSet — list seats, check availability, POST /api/seats/{id}/book/

BookingViewSet — create/list bookings, POST /api/bookings/clear/ to clear current user’s bookings

Default permissions allow anonymous usage; anonymous requests are attributed to a fallback guest user internally.

Server-rendered UI (Bootstrap)

Pages: /movies/, /seats/, /history/

Theme inspired by Alien: Resurrection (neon acid-green, dark biotech vibes)

History page contains Clear My Bookings button wired to the API

Environment config

Uses django-environ with a .env file for secrets & settings

Works locally (SQLite) and on Render (Gunicorn + WhiteNoise static)

Testing

Unit tests for models (string repr, defaults, booking behavior, uniqueness)

Integration tests against API endpoints (status codes & payloads)

Project Structure (key files)

movie_theater_booking/
├─ manage.py
├─ Procfile                 # for Render (production server via gunicorn)
├─ requirements.txt         # dependencies
├─ bookings/
│  ├─ settings.py           # uses django-environ; WhiteNoise for static
│  ├─ urls.py               # page routes + DRF router
│  ├─ wsgi.py
│  ├─ models.py             # Movie, Seat, Booking
│  ├─ serializers.py        # DRF serializers
│  ├─ views.py              # ViewSets + template views + clear action
│  ├─ templates/
│  │  └─ bookings/
│  │     ├─ base.html       # themed Bootstrap shell
│  │     ├─ movies.html
│  │     ├─ seats.html
│  │     └─ history.html    # with “Clear My Bookings”
│  ├─ fixtures/
│  │  ├─ movies.json        # Alien/Predator/AVP films (optional)
│  │  └─ seats.json         # A–E x 1–10 seats (optional)
│  └─ tests.py              # unit + integration tests
└─ .env                     # local dev env vars (not committed)

Setup (local)

Python env & install
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

env (local only; keep out of Git)
DEBUG=True
DJANGO_KEY=your-very-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost,http://127.0.0.1

Load demo data
python manage.py loaddata bookings/fixtures/movies.json
python manage.py loaddata bookings/fixtures/seats.json

Migrate & run
python manage.py migrate
python manage.py runserver 0.0.0.0:3000

Testing
Run all tests (unit + integration):

python manage.py test bookings -v 2

What’s covered:

Model tests: defaults, __str__, seat auto-booking on Booking.save(), duplicate protection

API tests: list endpoints, availability, booking success, conflict on double booking, history list


Deployment — Render

Files at project root (same folder as manage.py):

requirements.txt

Django==4.2.11
djangorestframework
django-environ
gunicorn
whitenoise


Procfile

web: gunicorn bookings.wsgi:application

bookings/settings.py additions

 --Static/WhiteNoise--
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # after SecurityMiddleware
    # ...
]

AI was used in the creation of this project to: draft bulk code according to given instruction, help assess and find root causes when debugging (saves a ton of time digging through documentation), translate syntax. sum up rough notes into a readable doc. 