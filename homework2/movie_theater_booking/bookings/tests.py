from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework import status

from .models import Movie, Seat, Booking

User = get_user_model()


class ModelTests(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title="Alien",
            description="Xeno on the Nostromo",
            release_date="1979-05-25",
            duration=117,
        )
        self.seat = Seat.objects.create(seat_number="A1")

        # a real user (not required for app logic, but nice to test)
        self.user = User.objects.create_user(username="ripley", password="xeno")

    def test_movie_str_and_ordering(self):
        Movie.objects.create(
            title="Aliens", description="Back to LV-426", release_date="1986-07-18", duration=137
        )
        titles = list(Movie.objects.values_list("title", flat=True))
        self.assertEqual(self.movie.__str__(), "Alien")
        # ordering = ["title"] in Meta -> Aliens then Alien (A comes before AI? actually "Alien" < "Aliens")
        self.assertEqual(titles, sorted(titles))

    def test_seat_defaults(self):
        self.assertEqual(self.seat.booking_status, Seat.BookingStatus.AVAILABLE)
        self.assertIsNotNone(self.seat.created_at)
        self.assertIsNotNone(self.seat.updated_at)

    def test_booking_marks_seat_booked(self):
        b = Booking.objects.create(
            movie=self.movie, seat=self.seat, user=self.user, booking_date=timezone.now()
        )
        self.seat.refresh_from_db()
        self.assertEqual(b.seat.booking_status, Seat.BookingStatus.BOOKED)
        self.assertEqual(self.seat.booking_status, Seat.BookingStatus.BOOKED)

    def test_cannot_double_book_same_seat(self):
        Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        with self.assertRaises(Exception):
            Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)


class APITests(TestCase):
    """
    Uses app’s current behavior:
      - Anonymous users are allowed.
      - Anonymous bookings are saved under the 'guest' user created on demand.
    """
    def setUp(self):
        self.client = APIClient()
        self.movie = Movie.objects.create(
            title="Alien Resurrection",
            description="USM Auriga experiments",
            release_date="1997-11-26",
            duration=109,
        )
        self.seat = Seat.objects.create(seat_number="B2")

    def test_movies_list_ok(self):
        r = self.client.get("/api/movies/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        data = r.json()
        items = data if isinstance(data, list) else (data.get("results") or [])
        self.assertTrue(any(m.get("title") == "Alien Resurrection" for m in items))

    def test_seats_available(self):
        r = self.client.get("/api/seats/available/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        data = r.json()
        items = data if isinstance(data, list) else (data.get("results") or [])
        # seat should be available initially
        self.assertTrue(any(s.get("seat_number") == "B2" for s in items))

    def test_book_seat_creates_booking(self):
        r = self.client.post(f"/api/seats/{self.seat.id}/book/", {"movie": self.movie.id}, format="json")
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.seat.refresh_from_db()
        self.assertEqual(self.seat.booking_status, Seat.BookingStatus.BOOKED)

    def test_double_book_conflict(self):
        # first booking
        self.client.post(f"/api/seats/{self.seat.id}/book/", {"movie": self.movie.id}, format="json")
        # try again
        r2 = self.client.post(f"/api/seats/{self.seat.id}/book/", {"movie": self.movie.id}, format="json")
        self.assertEqual(r2.status_code, status.HTTP_409_CONFLICT)

    def test_booking_history_endpoint(self):
        # creates a booking under 'guest'
        self.client.post(f"/api/seats/{self.seat.id}/book/", {"movie": self.movie.id}, format="json")
        r = self.client.get("/api/bookings/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        data = r.json()
        items = data if isinstance(data, list) else (data.get("results") or [])
        self.assertTrue(len(items) >= 1)
        self.assertEqual(items[0]["movie"]["title"], "Alien Resurrection")
