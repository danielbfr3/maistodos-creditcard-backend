from creditcards.views import CreditcardListCreateRetrieveView
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", CreditcardListCreateRetrieveView, basename="creditcard")

app_name = "creditcards"

urlpatterns = [
    path("", include(router.urls)),
]
