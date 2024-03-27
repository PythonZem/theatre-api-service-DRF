from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .models import (
    Actor,
    Genre,
    TheatreHall,
    Reservation,
    Play,
    Performance,
)
from .serializers import (
    ActorSerializer,
    GenreSerializer,
    PlaySerializer,
    PerformanceSerializer,
    ReservationSerializer,
    TheatreHallSerializer,
)


class ActorViewSet(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class PlayViewSet(ModelViewSet):
    queryset = Play.objects.all()
    serializer_class = PlaySerializer


class TheatreHallViewSet(ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer


class ReservationViewSet(ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class PerformanceViewSet(ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
