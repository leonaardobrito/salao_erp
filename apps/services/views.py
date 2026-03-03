from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# View temporária
def health_check(request):
    return JsonResponse({"status": "ok", "app": "services"})

# ViewSet temporário (será implementado depois)
class ServicesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        return JsonResponse({"message": "Lista de services"})
