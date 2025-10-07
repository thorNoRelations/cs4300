from django.contrib import admin
from .models import Movie, Seat, Booking


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_date", "duration")
    search_fields = ("title",)
    list_filter = ("release_date",)


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ("seat_number", "booking_status")
    list_filter = ("booking_status",)
    search_fields = ("seat_number",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("movie", "seat", "user", "booking_date")
    list_filter = ("movie", "booking_date")
    search_fields = ("movie__title", "seat__seat_number", "user__username")
    autocomplete_fields = ("movie", "seat", "user")
