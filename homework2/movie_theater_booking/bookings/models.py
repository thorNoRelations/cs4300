from django.conf import settings
from django.db import models
from django.utils import timezone


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    release_date = models.DateField()
    # duration in minutes (e.g., 142)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Seat(models.Model):
    class BookingStatus(models.TextChoices):
        AVAILABLE = "available", "Available"
        BOOKED = "booked", "Booked"

    # Keep seat numbers simple like "A1", "B12" or numeric "1", "2"
    seat_number = models.CharField(max_length=10, unique=True)
    booking_status = models.CharField(
        max_length=9,
        choices=BookingStatus.choices,
        default=BookingStatus.AVAILABLE,
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["seat_number"]

    def __str__(self):
        return f"Seat {self.seat_number} ({self.get_booking_status_display()})"


class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="bookings")
    seat = models.ForeignKey(Seat, on_delete=models.PROTECT, related_name="bookings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    booking_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now) 

    class Meta:
        ordering = ["-booking_date"]
        # Prevent the exact same (movie, seat) from being double-booked at the data layer
        unique_together = ("movie", "seat")

    def __str__(self):
        return f"{self.user} → {self.movie} @ {self.seat} on {self.booking_date:%Y-%m-%d %H:%M}"

    def clean(self):
        """
        Business rule (simple version since we don't have showtimes):
        - If a seat is marked BOOKED, block new bookings for it.
        - unique_together also ensures Movie+Seat cannot duplicate.
        """
        from django.core.exceptions import ValidationError

        if self.seat.booking_status == Seat.BookingStatus.BOOKED:
            raise ValidationError({"seat": "This seat is already booked."})

    def save(self, *args, **kwargs):
        # Validate first (raises on conflict)
        self.full_clean()

        # Save the booking
        super().save(*args, **kwargs)

        # Mark seat as booked if it isn’t already
        if self.seat.booking_status != Seat.BookingStatus.BOOKED:
            self.seat.booking_status = Seat.BookingStatus.BOOKED
            self.seat.save(update_fields=["booking_status", "updated_at"])
