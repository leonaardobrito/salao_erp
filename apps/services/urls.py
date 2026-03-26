# apps/services/urls.py
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.ServiceViewSet, basename='service')

urlpatterns = router.urls

__all__ = ['urlpatterns']
