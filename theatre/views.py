from datetime import datetime

from django.db.models import Count, F
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import (
    Actor,
    Genre,
    TheatreHall,
    Reservation,
    Play,
    Performance,
)
from .permissions import IsAdminOrIfAuthenticatedReadOnly
from .serializers import (
    ActorSerializer,
    GenreSerializer,
    PlaySerializer,
    PerformanceSerializer,
    ReservationSerializer,
    TheatreHallSerializer,
    PlayListSerializer,
    PlayDetailSerializer,
    PerformanceListSerializer,
    PerformanceDetailSerializer,
    ReservationListSerializer,
    PlayImageSerializer,
    ActorImageSerializer,
)


class ActorViewSet(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]
    authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        if self.action == "upload_image":
            return ActorImageSerializer
        return self.serializer_class


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]
    authentication_classes = [JWTAuthentication]


class PlayViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Play.objects.prefetch_related("actors", "genres")
    serializer_class = PlaySerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]
    authentication_classes = [JWTAuthentication]

    @staticmethod
    def _params_to_ints(qs):
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
        if self.action == "list":
            return PlayListSerializer

        if self.action == "retrieve":
            return PlayDetailSerializer

        if self.action == "upload_image":
            return PlayImageSerializer

        return PlaySerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
    )
    def upload_image(self, request, pk=None):
        play = self.get_object()
        serializer = self.get_serializer(play, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "genres",
                type={"type": "list", "items": {"type": OpenApiTypes.STR}},
                description="Filter by genre id (ex. ?genres=2,5)",
            ),
            OpenApiParameter(
                "actors",
                type={"type": "list", "items": {"type": OpenApiTypes.STR}},
                description="Filter by actor id (ex. ?actors=2,5)",
            ),
            OpenApiParameter(
                "title",
                type=OpenApiTypes.STR,
                description="Filter by movie title (ex. ?title=fiction)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class TheatreHallViewSet(ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]
    authentication_classes = [JWTAuthentication]


class PerformanceViewSet(ModelViewSet):
    queryset = (
        Performance.objects.all()
        .select_related("play", "theatre_hall")
        .annotate(
            tickets_available=(
                F("theatre_hall__rows") * F("theatre_hall__seats_in_row")
                - Count("tickets")
            )
        )
    )
    serializer_class = PerformanceSerializer

    def get_queryset(self):
        queryset = self.queryset

        if date := self.request.query_params.get("date"):
            date = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(show_time__date=date)

        if play_id := self.request.query_params.get("play"):
            queryset = queryset.filter(play_id=int(play_id))

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PerformanceListSerializer

        if self.action == "retrieve":
            return PerformanceDetailSerializer

        return PerformanceSerializer


class ReservationPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class ReservationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Reservation.objects.prefetch_related(
        "tickets__performance__play", "tickets__performance__theatre_hall"
    )
    serializer_class = ReservationSerializer
    pagination_class = ReservationPagination
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer

        return ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
