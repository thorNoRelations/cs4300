"""
URL configuration for bookings project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, SeatViewSet, BookingViewSet, movies_page, seats_page, history_page

router = DefaultRouter()
router.register(r"movies", MovieViewSet, basename="movie")
router.register(r"seats", SeatViewSet, basename="seat")
router.register(r"bookings", BookingViewSet, basename="booking")

urlpatterns = [
    path("api/", include(router.urls))

    path("api/", include(router.urls)),
    path("movies/", movies_page, name="movies_page"),
    path("seats/", seats_page, name="seats_page"),
    path("history/", history_page, name="history_page"),
]

