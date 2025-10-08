from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator

from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Movie, Seat, Booking
from .serializers import (
    MovieSerializer, SeatSerializer,
    BookingWriteSerializer, BookingReadSerializer
)

def _resolve_user(request):
    """Return an authenticated user if present; otherwise a shared 'guest' user."""
    if getattr(request, "user", None) and request.user.is_authenticated:
        return request.user
    User = get_user_model()
    guest, _ = User.objects.get_or_create(username="guest", defaults={"is_active": True})
    return guest


# ---------- API VIEWSETS ----------

from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.shortcuts import get_object_or_404
from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingWriteSerializer, BookingReadSerializer

def _resolve_user(request):
    """Return an authenticated user if present; otherwise a shared 'guest' user."""
    if getattr(request, "user", None) and request.user.is_authenticated:
        return request.user
    User = get_user_model()
    guest, _ = User.objects.get_or_create(username="guest", defaults={"is_active": True})
    return guest

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().order_by("title")
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]  # public

class SeatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Seat.objects.all().order_by("seat_number")
    serializer_class = SeatSerializer
    permission_classes = [permissions.AllowAny]  # public list/retrieve

    @action(detail=False, methods=["get"], permission_classes=[permissions.AllowAny])
    def available(self, request):
        qs = self.get_queryset().filter(booking_status=Seat.BookingStatus.AVAILABLE)
        page = self.paginate_queryset(qs)
        ser = self.get_serializer(page or qs, many=True)
        return self.get_paginated_response(ser.data) if page is not None else Response(ser.data)

    @action(detail=True, methods=["post"], permission_classes=[permissions.AllowAny])
    def book(self, request, pk=None):
        """Body: { "movie": <movie_id> }"""
        seat = self.get_object()
        movie_id = request.data.get("movie")
        if not movie_id:
            return Response({"detail": "Field 'movie' is required."}, status=status.HTTP_400_BAD_REQUEST)

        movie = get_object_or_404(Movie, pk=movie_id)
        user = _resolve_user(request)

        with transaction.atomic():
            seat_locked = Seat.objects.select_for_update().get(pk=seat.pk)
            if seat_locked.booking_status == Seat.BookingStatus.BOOKED:
                return Response({"detail": "Seat already booked."}, status=status.HTTP_409_CONFLICT)
            booking = Booking(user=user, movie=movie, seat=seat_locked)
            booking.full_clean()
            booking.save()
        return Response(BookingReadSerializer(booking).data, status=status.HTTP_201_CREATED)

class BookingViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]  # public create/list/retrieve

    def get_queryset(self):
        # If anonymous, show "guest" bookings; if logged in, show that user’s bookings.
        user = _resolve_user(self.request)
        return Booking.objects.filter(user=user).select_related("movie", "seat").order_by("-booking_date")

    def get_serializer_class(self):
        return BookingWriteSerializer if self.action == "create" else BookingReadSerializer

    def perform_create(self, serializer):
        user = _resolve_user(self.request)
        seat = serializer.validated_data["seat"]
        movie = serializer.validated_data["movie"]
        with transaction.atomic():
            seat_locked = Seat.objects.select_for_update().get(pk=seat.pk)
            if seat_locked.booking_status == Seat.BookingStatus.BOOKED:
                from django.core.exceptions import ValidationError
                raise ValidationError({"seat": "This seat is already booked."})
            serializer.save(user=user, seat=seat_locked, movie=movie)


# ---------- TEMPLATE (SERVER) VIEWS ----------


def movies_page(request):
    movies = Movie.objects.all().order_by("title")
    return render(request, "bookings/movies.html", {"movies": movies})

def seats_page(request):
    # Generic seat booking page (its JS calls /api/seats/ etc.)
    return render(request, "bookings/seats.html")


def history_page(request):
    return render(request, "bookings/history.html")