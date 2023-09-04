from core.views import CustomSpectacularAPIView
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", CustomSpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path("api/users/", include("users.urls")),
    path("api/creditcards/", include("creditcards.urls")),
]
