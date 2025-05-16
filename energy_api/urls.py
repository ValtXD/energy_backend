from django.urls import path, include
from rest_framework.routers import DefaultRouter
from energy_api.views import (
    AmbienteViewSet,
    EstadoViewSet,
    BandeiraViewSet,
    AparelhoViewSet
)

router = DefaultRouter()
router.register(r'ambientes', AmbienteViewSet)
router.register(r'estados', EstadoViewSet)
router.register(r'bandeiras', BandeiraViewSet)
router.register(r'aparelhos', AparelhoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]