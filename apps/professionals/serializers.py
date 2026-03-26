# apps/professionals/serializers.py
from rest_framework import serializers
from accounts.models import User
from .models import Professional


class ProfessionalListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.full_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)

    class Meta:
        model = Professional
        fields = [
            'id', 'name', 'email', 'phone',
            'commission_percent', 'color', 'specialties',
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ProfessionalDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.full_name', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)
    mobile = serializers.CharField(source='user.mobile', read_only=True)

    class Meta:
        model = Professional
        fields = [
            'id', 'user', 'name', 'first_name', 'last_name',
            'email', 'phone', 'mobile',
            'commission_percent', 'color', 'specialties',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class ProfessionalCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='professional', is_active=True)
    )

    class Meta:
        model = Professional
        fields = ['user', 'commission_percent', 'color', 'specialties']

    def validate_user(self, value):
        if Professional.objects.filter(user=value).exists():
            raise serializers.ValidationError(
                'Este usuário já possui um perfil profissional.'
            )
        return value


class ProfessionalUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = ['commission_percent', 'color', 'specialties', 'is_active']
