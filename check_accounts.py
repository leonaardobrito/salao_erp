#!/usr/bin/env python
"""
Script para verificar se o módulo accounts está completo
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.apps import apps
from django.urls import get_resolver

def check_module():
    print("\n🔍 VERIFICANDO MÓDULO ACCOUNTS...\n")
    
    # Dicionário para armazenar resultados
    results = {}
    
    # 1. Verificar se o app está instalado
    results['app_installed'] = apps.is_installed('accounts')
    print(f"📌 App instalado: {'✅' if results['app_installed'] else '❌'}")
    
    # 2. Verificar modelo User
    try:
        from accounts.models import User
        user = User.objects.first()
        results['model_user'] = True
        print("📌 Modelo User: ✅")
    except Exception as e:
        results['model_user'] = False
        print(f"📌 Modelo User: ❌ ({e})")
    
    # 3. Verificar serializer
    try:
        from accounts.serializers import UserCreateSerializer
        serializer = UserCreateSerializer()
        results['serializer'] = True
        print("📌 Serializer UserCreateSerializer: ✅")
    except Exception as e:
        results['serializer'] = False
        print(f"📌 Serializer UserCreateSerializer: ❌ ({e})")
    
    # 4. Verificar service
    try:
        from accounts.services import UserService
        service = UserService()
        results['service'] = True
        print("📌 Service UserService: ✅")
    except Exception as e:
        results['service'] = False
        print(f"📌 Service UserService: ❌ ({e})")
    
    # 5. Verificar repository
    try:
        from accounts.repositories import UserRepository
        repo = UserRepository()
        results['repository'] = True
        print("📌 Repository UserRepository: ✅")
    except Exception as e:
        results['repository'] = False
        print(f"📌 Repository UserRepository: ❌ ({e})")
    
    # 6. Verificar URLs
    print("\n📌 VERIFICANDO URLs DO ACCOUNTS")
    try:
        from accounts import urls as accounts_urls
        results['urls_module'] = len(accounts_urls.urlpatterns) > 0
        print(f"   ✅ Módulo accounts.urls tem {len(accounts_urls.urlpatterns)} URLs")
        
        # Verificar no resolver
        resolver = get_resolver()
        accounts_in_resolver = False
        url_patterns_found = []
        
        for pattern in resolver.url_patterns:
            pattern_str = str(pattern)
            if 'api/accounts/' in pattern_str or 'accounts.urls' in pattern_str:
                accounts_in_resolver = True
                url_patterns_found.append(pattern_str)
        
        if accounts_in_resolver:
            print(f"   ✅ URLs do accounts encontradas no resolver: {len(url_patterns_found)}")
            for url in url_patterns_found:
                print(f"      - {url}")
            results['urls_resolver'] = True
        else:
            print("   ❌ URLs do accounts NÃO encontradas no resolver")
            results['urls_resolver'] = False
            
    except Exception as e:
        results['urls_module'] = False
        results['urls_resolver'] = False
        print(f"   ❌ Erro ao verificar URLs: {e}")
    
    # 7. Verificar permissões
    try:
        from infrastructure.permissions import IsAdmin, IsOwnerOrAdmin
        results['permissions'] = True
        print("📌 Permissions: ✅")
    except Exception as e:
        results['permissions'] = False
        print(f"📌 Permissions: ❌ ({e})")
    
    # 8. Verificar exceptions
    try:
        from infrastructure.exceptions import custom_exception_handler
        results['exceptions'] = True
        print("📌 Exceptions: ✅")
    except Exception as e:
        results['exceptions'] = False
        print(f"📌 Exceptions: ❌ ({e})")
    
    # 9. Testar reverse de URLs
    print("\n📌 TESTANDO REVERSE DE URLs")
    try:
        from django.urls import reverse
        login_url = reverse('login')
        print(f"   ✅ URL de login: {login_url}")
        results['reverse_login'] = True
    except Exception as e:
        print(f"   ❌ Erro ao reverter 'login': {e}")
        results['reverse_login'] = False
    
    try:
        users_url = reverse('user-list')
        print(f"   ✅ URL user-list: {users_url}")
        results['reverse_userlist'] = True
    except Exception as e:
        print(f"   ❌ Erro ao reverter 'user-list': {e}")
        results['reverse_userlist'] = False
    
    # 10. Verificar view de login
    try:
        from accounts.views import CustomTokenObtainPairView
        results['login_view'] = True
        print("\n📌 View de login: ✅")
    except Exception as e:
        results['login_view'] = False
        print(f"\n📌 View de login: ❌ ({e})")
    
    print("\n" + "="*70)
    print("📊 RESUMO FINAL")
    print("="*70)
    
    # Lista completa de verificações
    checks = {
        'App instalado': results.get('app_installed', False),
        'Modelo User': results.get('model_user', False),
        'Serializer UserCreateSerializer': results.get('serializer', False),
        'Service UserService': results.get('service', False),
        'Repository UserRepository': results.get('repository', False),
        'URLs (módulo)': results.get('urls_module', False),
        'URLs (resolver)': results.get('urls_resolver', False),
        'Reverse login': results.get('reverse_login', False),
        'Reverse user-list': results.get('reverse_userlist', False),
        'View de login': results.get('login_view', False),
        'Permissions': results.get('permissions', False),
        'Exceptions': results.get('exceptions', False),
    }
    
    # Exibir cada verificação
    for check_name, check_result in checks.items():
        status = "✅" if check_result else "❌"
        print(f"{status} {check_name}")
    
    print("\n" + "="*70)
    
    # Verificação final
    essential_checks = [
        'app_installed',
        'model_user', 
        'serializer',
        'service',
        'repository',
        'urls_module',
        'reverse_login',
        'reverse_userlist'
    ]
    
    if all(results.get(check, False) for check in essential_checks):
        print("✅✅✅ MÓDULO ACCOUNTS COMPLETO E FUNCIONANDO! ✅✅✅")
    else:
        print("❌❌❌ MÓDULO ACCOUNTS COM PROBLEMAS ❌❌❌")
        print("\nProblemas encontrados:")
        
        if not results.get('app_installed'):
            print("   • App 'accounts' não está em INSTALLED_APPS")
        if not results.get('model_user'):
            print("   • Modelo User não pode ser importado")
        if not results.get('serializer'):
            print("   • Serializer UserCreateSerializer não pode ser importado")
        if not results.get('service'):
            print("   • Service UserService não pode ser importado")
        if not results.get('repository'):
            print("   • Repository UserRepository não pode ser importado")
        if not results.get('urls_module'):
            print("   • Módulo accounts.urls não encontrado ou vazio")
        if not results.get('reverse_login'):
            print("   • URL de login não está funcionando")
        if not results.get('reverse_userlist'):
            print("   • URL user-list não está funcionando")
        if not results.get('login_view'):
            print("   • View CustomTokenObtainPairView não encontrada")
        if not results.get('permissions'):
            print("   • Permissions não podem ser importadas")
        if not results.get('exceptions'):
            print("   • Exceptions não podem ser importadas")
    
    print("="*70 + "\n")

if __name__ == '__main__':
    check_module()