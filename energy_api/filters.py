from django_filters import rest_framework as filters
from .models import Aparelho


class AparelhoFilter(filters.FilterSet):
    nome = filters.CharFilter(field_name='nome', lookup_expr='icontains')

    potencia_min = filters.NumberFilter(field_name='potencia_watts', lookup_expr='gte')
    potencia_max = filters.NumberFilter(field_name='potencia_watts', lookup_expr='lte')

    tempo_uso_min = filters.NumberFilter(field_name='tempo_uso_diario_horas', lookup_expr='gte')
    tempo_uso_max = filters.NumberFilter(field_name='tempo_uso_diario_horas', lookup_expr='lte')

    quantidade_min = filters.NumberFilter(field_name='quantidade', lookup_expr='gte')
    quantidade_max = filters.NumberFilter(field_name='quantidade', lookup_expr='lte')

    ambiente = filters.NumberFilter(field_name='ambiente', lookup_expr='exact')
    estado = filters.NumberFilter(field_name='estado', lookup_expr='exact')
    bandeira = filters.NumberFilter(field_name='bandeira', lookup_expr='exact')

    data_cadastro_min = filters.DateFilter(field_name='data_cadastro', lookup_expr='gte')
    data_cadastro_max = filters.DateFilter(field_name='data_cadastro', lookup_expr='lte')

    class Meta:
        model = Aparelho
        fields = []