from unittest.mock import patch

from django.contrib import admin
from django.urls import path, include

from energy_api.views import AparelhoViewSet, UserProfileViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('energy_api.urls')),
    path('api/aparelhos/', AparelhoViewSet.as_view, name='adicionar-aparelho'),
    path('api/user/', UserProfileViewSet.as_view, name='adicionar-user'),
]
