from rest_framework import serializers
from django.utils import timezone
from .models import Aparelho, Ambiente, Estado, Bandeira

class AparelhoCreateSerializer(serializers.ModelSerializer):
    ambiente = serializers.PrimaryKeyRelatedField(queryset=Ambiente.objects.all())
    estado = serializers.PrimaryKeyRelatedField(queryset=Estado.objects.all())
    bandeira = serializers.PrimaryKeyRelatedField(queryset=Bandeira.objects.all())

    class Meta:
        model = Aparelho
        fields = '__all__'
        extra_kwargs = {
            'data_cadastro': {'required': False}
        }

    def create(self, validated_data):
        validated_data['data_cadastro'] = validated_data.get('data_cadastro') or timezone.now().date()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class AmbienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambiente
        fields = ['id', 'nome']


class EstadoSerializer(serializers.ModelSerializer):
    tarifa_valor = serializers.DecimalField(
        source='tarifa.valor_kwh',
        max_digits=6,
        decimal_places=5,
        read_only=True
    )

    class Meta:
        model = Estado
        fields = ['id', 'nome', 'sigla', 'tarifa_valor']


class BandeiraSerializer(serializers.ModelSerializer):
    cor_display = serializers.CharField(source='get_cor_display')

    class Meta:
        model = Bandeira
        fields = ['id', 'cor', 'cor_display', 'valor_adicional', 'descricao']


class AparelhoSerializer(serializers.ModelSerializer):
    ambiente = AmbienteSerializer()
    estado = EstadoSerializer()
    bandeira = BandeiraSerializer()

    class Meta:
        model = Aparelho
        fields = '__all__'