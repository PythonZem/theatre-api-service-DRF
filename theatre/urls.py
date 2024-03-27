from django.urls import path, include
from rest_framework import routers

from .views import (
    ActorViewSet,
    GenreViewSet,
    PerformanceViewSet,
    PlayViewSet,
    TheatreHallViewSet,
    ReservationViewSet,

)

router = routers.DefaultRouter()
router.register("actors", ActorViewSet)
router.register("genres", GenreViewSet)
router.register("performances", PerformanceViewSet)
router.register("plays", PlayViewSet)
router.register("theatrehalls", TheatreHallViewSet)
router.register("reservations", ReservationViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "theatre"
