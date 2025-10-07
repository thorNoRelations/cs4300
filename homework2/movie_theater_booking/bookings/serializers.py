from rest_framework import serializers
from .models import Movie, Seat, Booking

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title", "description", "release_date", "duration", "created_at", "updated_at"]

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ["id", "seat_number", "booking_status", "created_at", "updated_at"]

class BookingWriteSerializer(serializers.ModelSerializer):
    """Used when creating a booking."""
    class Meta:
        model = Booking
        fields = ["id", "movie", "seat", "booking_date"]

class BookingReadSerializer(serializers.ModelSerializer):
    """Used for listing/retrieving bookings."""
    movie = MovieSerializer(read_only=True)
    seat = SeatSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ["id", "movie", "seat", "booking_date", "created_at"]
