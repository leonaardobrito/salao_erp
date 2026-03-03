# apps/accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.contrib.auth import authenticate
from .models import User, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer para o perfil do usuário"""
    
    class Meta:
        model = UserProfile
        fields = [
            'address', 'address_number', 'complement',
            'neighborhood', 'city', 'state', 'zip_code',
            'receive_newsletter', 'receive_notifications', 'avatar'
        ]


class UserListSerializer(serializers.ModelSerializer):
    """Serializer para listagem de usuários (campos resumidos)"""
    
    full_name = serializers.SerializerMethodField()
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'full_name', 'first_name', 'last_name',
            'role', 'phone', 'mobile', 'is_active', 'profile', 'last_access'
        ]
        read_only_fields = ['id', 'last_access']
    
    def get_full_name(self, obj):
        return obj.full_name


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer para detalhes do usuário (campos completos)"""
    
    full_name = serializers.SerializerMethodField()
    profile = UserProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'full_name', 'first_name', 'last_name',
            'role', 'phone', 'mobile', 'document', 'birth_date',
            'is_active', 'date_joined', 'last_login', 'last_access',
            'created_at', 'updated_at', 'notes', 'profile'
        ]
        read_only_fields = [
            'id', 'date_joined', 'last_login', 'last_access',
            'created_at', 'updated_at'
        ]
    
    def get_full_name(self, obj):
        return obj.full_name
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        user = User.objects.create_user(**validated_data)
        
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)
        
        return user
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        
        # Atualizar campos do usuário
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Atualizar ou criar perfil
        if profile_data:
            profile, created = UserProfile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de usuário com senha"""
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label='Confirmar senha'
    )
    profile = UserProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password2',
            'first_name', 'last_name', 'role', 'phone', 'mobile',
            'document', 'birth_date', 'profile'
        ]
    
    def validate(self, attrs):
        """Validar senhas e outros campos"""
        # Validar senhas
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password': 'As senhas não conferem.'
            })
        
        # Validar força da senha
        try:
            validate_password(attrs['password'])
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError({
                'password': list(e.messages)
            })
        
        # Validar email único
        if User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({
                'email': 'Este email já está em uso.'
            })
        
        return attrs
    
    def create(self, validated_data):
        """Create user with encrypted password."""
        # 🔥 Já removemos password2 na validação, mas garantir
        validated_data.pop('password2', None)
        
        # Extrair profile data
        profile_data = validated_data.pop('profile', {})
        
        # Criar usuário
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        
        # Criar perfil
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)
        
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer para atualização de usuário"""
    
    profile = UserProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'mobile',
            'document', 'birth_date', 'notes', 'profile'
        ]
    
    def validate_email(self, value):
        """Validar email único (exceto para o próprio usuário)"""
        if User.objects.exclude(pk=self.instance.pk).filter(email=value).exists():
            raise serializers.ValidationError('Este email já está em uso.')
        return value


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer para alteração de senha"""
    
    old_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    new_password2 = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        label='Confirmar nova senha'
    )
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({
                'new_password': 'As senhas não conferem.'
            })
        
        try:
            validate_password(attrs['new_password'])
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError({
                'new_password': list(e.messages)
            })
        
        return attrs


class LoginSerializer(serializers.Serializer):
    """Serializer para login"""
    
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError(
                    'Credenciais inválidas.',
                    code='authorization'
                )
            
            if not user.is_active:
                raise serializers.ValidationError(
                    'Usuário inativo.',
                    code='authorization'
                )
            
            attrs['user'] = user
            return attrs
        
        raise serializers.ValidationError(
            'Informe usuário e senha.',
            code='authorization'
        )