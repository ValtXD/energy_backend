from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import datetime

from .filters import AparelhoFilter
from .models import Ambiente, Estado, Bandeira, Aparelho
from .serializers import (
    AmbienteSerializer,
    EstadoSerializer,
    BandeiraSerializer,
    AparelhoSerializer,
    AparelhoCreateSerializer
)


class AmbienteViewSet(viewsets.ModelViewSet):
    queryset = Ambiente.objects.all()
    serializer_class = AmbienteSerializer


class EstadoViewSet(viewsets.ModelViewSet):
    queryset = Estado.objects.filter(tarifa__isnull=False).select_related('tarifa')
    serializer_class = EstadoSerializer


class BandeiraViewSet(viewsets.ModelViewSet):
    queryset = Bandeira.objects.all()
    serializer_class = BandeiraSerializer


class AparelhoViewSet(viewsets.ModelViewSet):
    queryset = Aparelho.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nome', 'ambiente', 'estado', 'bandeira']
    filterset_class = AparelhoFilter

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AparelhoCreateSerializer
        return AparelhoSerializer

    @action(detail=False, methods=['get'])
    def by_date(self, request):
        date_str = request.query_params.get('date')
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                aparelhos = self.queryset.filter(data_cadastro=date_obj)
                serializer = self.get_serializer(aparelhos, many=True)
                return Response(serializer.data)
            except ValueError:
                return Response({"error": "Formato de data inválido"}, status=400)
        return Response({"error": "Parâmetro 'date' não fornecido"}, status=400)

    @action(detail=True, methods=['delete'])
    def remove(self, request, pk=None):
        aparelho = self.get_object()
        data_cadastro = aparelho.data_cadastro
        ambiente = aparelho.ambiente
        aparelho.delete()

        # Atualize histórico conforme sua lógica
        self.atualizar_historico(ambiente, data_cadastro)

        return Response({"status": "Aparelho removido com sucesso"})

    def atualizar_historico(self, ambiente, data_cadastro):
        # Implementar sua lógica de atualização do histórico aqui
        pass