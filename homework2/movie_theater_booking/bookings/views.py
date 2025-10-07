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


@login_required
def movie_list_page(request):
    movies = Movie.objects.all().order_by("title")
    return render(request, "bookings/movie_list.html", {"movies": movies})

@login_required
def seat_booking_page(request, movie_id: int):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, "bookings/seat_booking.html", {"movie": movie})

@login_required
def booking_history_page(request):
    return render(request, "bookings/booking_history.html")
# ---------- API VIEWSETS ----------

class MovieViewSet(viewsets.ModelViewSet):
    """
    CRUD for movies.
    """
    queryset = Movie.objects.all().order_by("title")
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]


class SeatViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List & retrieve seats; includes `available` and `book` actions.
    """
    queryset = Seat.objects.all().order_by("seat_number")
    serializer_class = SeatSerializer

    @action(detail=False, methods=["get"])
    def available(self, request):
        qs = self.get_queryset().filter(booking_status=Seat.BookingStatus.AVAILABLE)
        page = self.paginate_queryset(qs)
        ser = self.get_serializer(page or qs, many=True)
        return self.get_paginated_response(ser.data) if page is not None else Response(ser.data)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def book(self, request, pk=None):
        """
        Book this specific seat for a given movie.
        Body: { "movie": <movie_id> }
        """
        seat = self.get_object()
        movie_id = request.data.get("movie")
        if not movie_id:
            return Response({"detail": "Field 'movie' is required."}, status=status.HTTP_400_BAD_REQUEST)

        movie = get_object_or_404(Movie, pk=movie_id)

        try:
            with transaction.atomic():
                # Lock the seat row to prevent race conditions
                seat_locked = Seat.objects.select_for_update().get(pk=seat.pk)
                if seat_locked.booking_status == Seat.BookingStatus.BOOKED:
                    return Response({"detail": "Seat already booked."}, status=status.HTTP_409_CONFLICT)

                booking = Booking(user=request.user, movie=movie, seat=seat_locked)
                booking.full_clean()
                booking.save()  # flips seat to BOOKED in Booking.save()
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(BookingReadSerializer(booking).data, status=status.HTTP_201_CREATED)


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return getattr(obj, "user_id", None) == request.user.id


class BookingViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """
    Users can create bookings and list their own booking history.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related("movie", "seat").order_by("-booking_date")

    def get_serializer_class(self):
        if self.action == "create":
            return BookingWriteSerializer
        return BookingReadSerializer

    def perform_create(self, serializer):
        # Enforce seat availability atomically
        seat = serializer.validated_data["seat"]
        movie = serializer.validated_data["movie"]
        with transaction.atomic():
            seat_locked = Seat.objects.select_for_update().get(pk=seat.pk)
            if seat_locked.booking_status == Seat.BookingStatus.BOOKED:
                from django.core.exceptions import ValidationError
                raise ValidationError({"seat": "This seat is already booked."})

            booking = serializer.save(user=self.request.user, seat=seat_locked, movie=movie)
            # Booking.save() will flip the seat status to BOOKED
            return booking

# ---------- TEMPLATE (SERVER) VIEWS ----------

@method_decorator(login_required, name="dispatch")
def movies_page(request):
    """
    Server-rendered page; JS fetches /api/movies/ and paints.
    """
    return render(request, "bookings/movies.html")

@method_decorator(login_required, name="dispatch")
def seats_page(request):
    return render(request, "bookings/seats.html")

@method_decorator(login_required, name="dispatch")
def history_page(request):
    return render(request, "bookings/history.html")
