from django.contrib import admin

from .models import (
    Actor,
    Genre,
    TheatreHall,
    Reservation,
    Play,
    Performance,
    Ticket
)

admin.site.register(Actor)
admin.site.register(Genre)
admin.site.register(TheatreHall)
admin.site.register(Reservation)
admin.site.register(Play)
admin.site.register(Performance)
admin.site.register(Ticket)
