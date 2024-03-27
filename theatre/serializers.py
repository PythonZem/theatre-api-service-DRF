from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import (
    Actor,
    Genre,
    TheatreHall,
    Reservation,
    Play,
    Performance,
    Ticket,
)


class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name", "full_name")


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ("id", "name")


class PlaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Play
        fields = ("id", "title", "description", "actors", "genres")


class TheatreHallSerializer(serializers.ModelSerializer):

    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row")


class PerformanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Performance
        fields = ("id", "play", "theatre_hall", "show_time")


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ("id", "created_at", "user")


class TicketSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["performance"].theatrehall,
            ValidationError
        )
        return data

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "performance")
