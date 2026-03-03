# apps/accounts/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import User, UserProfile
from .services import UserService

User = get_user_model()


class UserModelTests(TestCase):
    """Testes para o modelo User"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
    
    def test_create_user(self):
        """Testa criação de usuário"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
    
    def test_full_name_property(self):
        """Testa propriedade full_name"""
        self.assertEqual(self.user.full_name, 'Test User')
        
        # Sem nome
        user2 = User.objects.create_user(
            username='test2',
            email='test2@example.com',
            password='testpass123'
        )
        self.assertEqual(user2.full_name, 'test2')
    
    def test_is_admin_property(self):
        """Testa propriedade is_admin"""
        self.assertFalse(self.user.is_admin)
        
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.assertTrue(admin.is_admin)
    
    def test_str_representation(self):
        """Testa representação string"""
        self.assertEqual(str(self.user), 'Test User')


class UserServiceTests(TestCase):
    """Testes para o UserService"""
    
    def setUp(self):
        self.service = UserService()
        self.user_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'Test@123456',
            'first_name': 'New',
            'last_name': 'User'
        }
    
    def test_create_user(self):
        """Testa criação de usuário via service"""
        user = self.service.create_user(self.user_data)
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'new@example.com')
    
    def test_create_duplicate_email(self):
        """Testa criação com email duplicado"""
        self.service.create_user(self.user_data)
        
        with self.assertRaises(Exception) as context:
            self.service.create_user(self.user_data)
        
        self.assertIn('Email já cadastrado', str(context.exception))
    
    def test_get_user_not_found(self):
        """Testa busca de usuário inexistente"""
        with self.assertRaises(Exception) as context:
            self.service.get_user(99999)
        
        self.assertIn('não encontrado', str(context.exception))


class UserAPITests(APITestCase):
    """Testes para a API de usuários"""
    
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'apiuser',
            'email': 'api@example.com',
            'password': 'Api@123456',
            'password2': 'Api@123456',
            'first_name': 'API',
            'last_name': 'User'
        }
        
        # Criar usuário admin
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        
        # Criar usuário comum
        self.user = User.objects.create_user(
            username='common',
            email='common@example.com',
            password='common123'
        )
    
    def test_create_user_api(self):
        """Testa criação de usuário via API"""
        url = reverse('user-list')
        response = self.client.post(url, self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)  # admin + common + novo
    
    def test_login_api(self):
        """Testa login via API"""
        url = reverse('login')
        data = {
            'username': 'common',
            'password': 'common123'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_login_invalid_credentials(self):
        """Testa login com credenciais inválidas"""
        url = reverse('login')
        data = {
            'username': 'common',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_me_endpoint_authenticated(self):
        """Testa endpoint /me com autenticação"""
        # Autenticar
        self.client.force_authenticate(user=self.user)
        
        url = reverse('user-me')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'common')
    
    def test_me_endpoint_unauthenticated(self):
        """Testa endpoint /me sem autenticação"""
        url = reverse('user-me')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_professionals_list(self):
        """Testa listagem de profissionais"""
        # Criar alguns profissionais
        User.objects.create_user(
            username='prof1',
            email='prof1@example.com',
            password='test123',
            role='professional'
        )
        User.objects.create_user(
            username='prof2',
            email='prof2@example.com',
            password='test123',
            role='professional'
        )
        
        self.client.force_authenticate(user=self.admin)
        url = reverse('user-professionals')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)