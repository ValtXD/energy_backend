from django.contrib import admin
from .models import Ambiente, Estado, Tarifa, Bandeira, TarifaSocial, Aparelho, HistoricoConsumo

# Registre cada modelo
admin.site.register(Ambiente)
admin.site.register(Estado)
admin.site.register(Tarifa)
admin.site.register(Bandeira)
admin.site.register(TarifaSocial)
admin.site.register(Aparelho)
admin.site.register(HistoricoConsumo)