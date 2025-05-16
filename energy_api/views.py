from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Ambiente, Estado, Bandeira, Aparelho
from .serializers import (
    AmbienteSerializer,
    EstadoSerializer,
    BandeiraSerializer,
    AparelhoSerializer,
    AparelhoCreateSerializer
)
from django.utils import timezone
from datetime import datetime


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
    queryset = Aparelho.objects.all().order_by('-data_cadastro')

    def get_serializer_class(self):
        if self.action == 'create':
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

        # Atualiza histórico (implemente esta função conforme sua lógica)
        self.atualizar_historico(ambiente, data_cadastro)

        return Response({"status": "Aparelho removido com sucesso"})