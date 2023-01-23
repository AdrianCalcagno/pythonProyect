from django.contrib import admin
from django.urls import path, include
from appFamiliares.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("appFamiliares.urls")),
    path("appFamiliares/", include("appFamiliares.urls")),
    path("", include("App2.urls")),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)