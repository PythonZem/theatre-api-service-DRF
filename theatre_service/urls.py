from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from theatre_service import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/theatre/', include("theatre.urls", namespace="theatre")),
    path("api/user/", include("user.urls", namespace="user")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
