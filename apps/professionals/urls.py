# apps/professionals/urls.py
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.ProfessionalViewSet, basename='professional')

urlpatterns = router.urls

__all__ = ['urlpatterns']
