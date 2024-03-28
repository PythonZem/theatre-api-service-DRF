from django.shortcuts import render
from rest_framework import mixins, viewsets
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
    PlayListSerializer,
    PlayDetailSerializer,
)


class ActorViewSet(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class PlayViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Play.objects.prefetch_related("actors", "genres")
    serializer_class = PlaySerializer

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        queryset = self.queryset

        if title := self.request.query_params.get("title"):
            queryset = queryset.filter(title__icontains=title)

        if actor := self.request.query_params.get("actor"):
            actors_id = self._params_to_ints(actor)
            queryset = queryset.filter(actor__id__in=actors_id)

        if genre := self.request.query_params.get("genres"):
            genres_id = self._params_to_ints(genre)
            queryset = queryset.filter(genre__id__in=genres_id)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "List":
            return PlayListSerializer

        if self.action == "retrieve":
            return PlayDetailSerializer

        return PlaySerializer


class TheatreHallViewSet(ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer


class ReservationViewSet(ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class PerformanceViewSet(ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
