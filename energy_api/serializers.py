from django.contrib.auth.models import User
from rest_framework import serializers
from django.utils import timezone


from .models import Aparelho, Ambiente, Estado, Bandeira, UserProfile, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'telefone', 'endereco', 'data_nascimento', 'cpf', 'genero', 'profissao']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)

        # Se o usuário já tem perfil, apenas atualize (isso não deveria acontecer na criação, mas só para garantir)
        profile, created = UserProfile.objects.get_or_create(user=user, defaults=validated_data)
        if not created:
            for attr, value in validated_data.items():
                setattr(profile, attr, value)
            profile.save()

        return profile

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